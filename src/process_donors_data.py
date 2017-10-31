
import sys
import copy
import pandas as pd
from helper_functions import *
from rolling_median import *


# read arguments for shell script
input_filename = sys.argv[1]
output_filename_zip = sys.argv[2]
output_filename_date = sys.argv[3]

# relevant indeces for the given file format
CMTE_ID_index = 0
ZIP_CODE_index = 10
DATE_index = 13
TRANSACTION_AMT_index = 14
OTHER_ID_index = 15
TOTAL_COLUMNS = 21


# prepare data for processing by getting the relevant data
def get_relevant_entries(all_entries_list):
    
    relevant_indeces = [CMTE_ID_index, ZIP_CODE_index, DATE_index, TRANSACTION_AMT_index]
    relevant_entries_list = []
    
    for index in relevant_indeces:
        relevant_entries_list.append(all_entries_list[index])
            
    return relevant_entries_list


# create a dictionary entry for a new ID
def create_id_entry(current_id, current_zip, current_date, current_contrib):
    
    if is_zip_valid(current_zip) or is_date_valid(current_date):
        recipient_info_dict[current_id] = []
        roll_median = RollingMedian()
        
        if is_zip_valid(current_zip):
            current_zip = format_zip(current_zip)
            roll_median.add(current_contrib)
            recipient_info_dict[current_id].append({current_zip: copy.deepcopy(roll_median)})
            
            write_to_zipcode_file(current_id, 
                              current_zip, 
                              current_contrib, 
                              1, 
                              current_contrib)
            
        else:
            recipient_info_dict[current_id].append({})

        if is_date_valid(current_date):
            roll_median = RollingMedian()
            roll_median.add(current_contrib)
            recipient_info_dict[current_id].append({current_date: copy.deepcopy(roll_median)})
        else:
            recipient_info_dict[current_id].append({})
        

# create a dictionary entry for a new date (existing ID)
def create_date_entry(current_id, current_date, current_contrib):
                             
    if is_date_valid(current_date):
        roll_median = RollingMedian()
        roll_median.add(current_contrib)
        recipient_info_dict[current_id][1][current_date] = copy.deepcopy(roll_median)
        

# create a dictionary entry for a new zip (existing ID)
def create_zip_entry(current_id, current_zip, current_date, current_contrib):
                             
    if is_zip_valid(current_zip):
        current_zip = format_zip(current_zip)
        roll_median = RollingMedian()
        roll_median.add(current_contrib)
        recipient_info_dict[current_id][0][current_zip] = copy.deepcopy(roll_median)
        
        write_to_zipcode_file(current_id, 
                              current_zip, 
                              current_contrib, 
                              1, 
                              current_contrib)

                             
def write_to_zipcode_file(current_id, current_zip, median, num_so_far, total):

    line_to_write = "{0}|{1}|{2}|{3}|{4}\n".format(current_id, current_zip, median, num_so_far, total)
    output_file_zip.write(line_to_write)



if __name__ == "__main__":
    
    input_file = open(input_filename, 'r')
    output_file_zip = open(output_filename_zip, 'w')


    dataframe_dict = {"ID":[], "Date":[], "Median":[], "Number Contributions":[], "Total":[]}
    recipient_info_dict = {}

    # recipient_info_dict = {'id1':[{'zip1': roll_median_zip1, 'zip2': roll_median_zip2, ...},
    #                           {'date1': roll_median_date1, 'date2': roll_median_date2, ...}],
    #                       'id2':[{'zip1': roll_median_zip1, 'zip2': roll_median_zip2, ...},
    #                          {'date1': roll_median_date1, 'date2': roll_median_date2, ...}], ...other id's}

    next = input_file.readline()
    while next != '':
        if next != '\n':
            input_line = next.split('|')
            
            # only consider the record if OTHER_ID is empty, CMTE_ID is non-empty, and TRANSACTION_AMT is non-empty
            if len(input_line) == TOTAL_COLUMNS and input_line[OTHER_ID_index] == ''         and input_line[CMTE_ID_index] != '' and input_line[TRANSACTION_AMT_index] !='' and is_amount_valid(input_line[TRANSACTION_AMT_index]):
                
                input_line[-1] = input_line[-1].rstrip() # remove newline character
                input_line_data_list = get_relevant_entries(input_line) # id, zip, date, contribution

                input_line_id = input_line_data_list[0]
                input_line_zip = input_line_data_list[1]
                input_line_date = input_line_data_list[2]
                input_line_contribution = int(input_line_data_list[3])


                if input_line_id in recipient_info_dict:
                    if input_line_zip.isnumeric():
                        input_line_zip = format_zip(input_line_zip)
                        if input_line_zip in recipient_info_dict[input_line_id][0]:
                            recipient_info_dict[input_line_id][0][input_line_zip].add(input_line_contribution)
                            
                            median = recipient_info_dict[input_line_id][0][input_line_zip].get_median()
                            num_contr = recipient_info_dict[input_line_id][0][input_line_zip].size
                            total = recipient_info_dict[input_line_id][0][input_line_zip].total
                            
                            write_to_zipcode_file(input_line_id,
                                              input_line_zip,
                                              median,
                                              num_contr,
                                              total)
                        else:
                            create_zip_entry(input_line_id, input_line_zip, input_line_date, input_line_contribution)


                    if input_line_date in recipient_info_dict[input_line_id][1]:
                        recipient_info_dict[input_line_id][1][input_line_date].add(input_line_contribution)

                    else:
                        create_date_entry(input_line_id, input_line_date, input_line_contribution)
                else:
                    create_id_entry(input_line_id, input_line_zip, input_line_date, input_line_contribution)
    
        next = input_file.readline()

    # create a DataFrame
    for key, dict_list in recipient_info_dict.items():
        for date in dict_list[1]:
            dataframe_dict["ID"].append(key)
            dataframe_dict["Date"].append(format_date(date))
            dataframe_dict["Median"].append(dict_list[1][date].get_median())
            dataframe_dict["Number Contributions"].append(dict_list[1][date].size)
            dataframe_dict["Total"].append(dict_list[1][date].total)

    df = pd.DataFrame(dataframe_dict, columns=["ID", "Date", "Median", "Number Contributions", "Total"])

    df["Date"] = pd.to_datetime(df.Date)

    # sort the DataFrame
    df.sort_values(by=["ID", "Date"], inplace=True)

    # write to medianvals_by_date.txt
    df.to_csv(output_filename_date,
              header=None, index=None, sep='|', date_format="%m%d%Y")

    # close all opened files
    output_file_zip.close()
    input_file.close()


