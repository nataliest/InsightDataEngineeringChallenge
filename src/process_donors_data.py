
# coding: utf-8

# <h1>Test notebook 1</h1>

# In[45]:


import pandas as pd
import sys
from datetime import date
import time
import math
import copy


# In[46]:


# read arguments for shell script
input_filename = sys.argv[1]
output_filename_zip = sys.argv[2]
output_filename_date = sys.argv[3]

CMTE_ID_index = 0
ZIP_CODE_index = 10
DATE_index = 13
TRANSACTION_AMT_index = 14
OTHER_ID_index = 15
TOTAL_COLUMNS = 21


# In[47]:


def format_relevant_entries(all_entries_list):
    
    relevant_indeces = [CMTE_ID_index, ZIP_CODE_index, DATE_index, TRANSACTION_AMT_index]
    relevant_entries_list = []
    
    for index in relevant_indeces:
        
        if index == 10 and len(all_entries_list[index]) > 5: # if provided zip-code has 9 digits, use only the first 5
            all_entries_list[index] = all_entries_list[index][:5]
            relevant_entries_list.append(all_entries_list[index][:5])        
        else:
            relevant_entries_list.append(all_entries_list[index])
            
    return relevant_entries_list


# In[48]:


def format_date(date):
    
    formatted = date[:2] + '/' + date[2:4] + '/' + date[4:]
    
    return formatted


# In[49]:


# calculate running median using red black tree

class Node:
    RED = True
    BLACK = False

    def __init__(self, key, color = RED):
        if not type(color) == bool:
            raise TypeError("Bad value for color parameter, expected True/False but given %s" % color)
        self.color = color
        self.key = key
        self.left = self.right = self.parent = NilNode.instance()

    def __str__(self, level = 0, indent = "   "):
        s = level * indent + str(self.key)
        if self.left:
            s = s + "\n" + self.left.__str__(level + 1, indent)
        if self.right:
            s = s + "\n" + self.right.__str__(level + 1, indent)
        return s

    def __nonzero__(self):
        return True

    def __bool__(self):
        return True


class NilNode(Node):
    __instance__ = None

    @classmethod
    def instance(self):
        if self.__instance__ is None:
            self.__instance__ = NilNode()
        return self.__instance__

    def __init__(self):
        self.color = Node.BLACK
        self.key = None
        self.left = self.right = self.parent = None

    def __nonzero__(self):
        return False

    def __bool__(self):
        return False

class RedBlackTree:
    def __init__(self):
        self.root = NilNode.instance()
        self.size = 0
        self.num_right_nodes = 0
        self.num_left_nodes = 0
        self.total = 0
    
    def __str__(self):
        return ("(root.size = %d)\n" % self.size)  + str(self.root) + " left: " + str(self.num_left_nodes) + " right " + str(self.num_right_nodes) 

    def add(self, key):
        self.insert(Node(key))
    
    def get_median(self):
        median = 0
        fract = 0
        dec = 0
        size = 1 + self.num_left_nodes + self.num_right_nodes
        if size == 1:
            median = self.root.key
            fract, dec = math.modf(median)
        elif self.num_right_nodes < self.num_left_nodes:
            median = (self.root.key + self.root.left.key) / 2
            fract, dec = math.modf(median)

        elif self.num_right_nodes > self.num_left_nodes:
            median = (self.root.key + self.root.right.key) / 2
            fract, dec = math.modf(median)
        elif self.num_right_nodes == self.num_left_nodes:
            median = self.root.key
            fract, dec = math.modf(median)
            
        if fract < 0.5:
            median = dec
        else:
            median = dec + 1
        return int(median)
    
    def insert(self, x):
        self.size += 1
        self.total += x.key

        if self.size % 2 == 1:
            self.num_left_nodes = self.size // 2
            self.num_right_nodes = self.num_left_nodes 
        else:       
            if self.size > 0:
                if x.key < self.root.key:
                    self.num_left_nodes += 1
                elif x.key >= self.root.key:
                    self.num_right_nodes += 1
                
        self.__insert_helper(x)

        x.color = Node.RED
        while x != self.root and x.parent.color == Node.RED:
            if x.parent == x.parent.parent.left:
                y = x.parent.parent.right
                if y and y.color == Node.RED:
                    x.parent.color = Node.BLACK
                    y.color = Node.BLACK
                    x.parent.parent.color = Node.RED
                    x = x.parent.parent
                else:
                    if x == x.parent.right:
                        x = x.parent
                        self.__left_rotate(x)
                    x.parent.color = Node.BLACK
                    x.parent.parent.color = Node.RED
                    self.__right_rotate(x.parent.parent)
            else:
                y = x.parent.parent.left
                if y and y.color == Node.RED:
                    x.parent.color = Node.BLACK
                    y.color = Node.BLACK
                    x.parent.parent.color = Node.RED
                    x = x.parent.parent
                else:
                    if x == x.parent.left:
                        x = x.parent
                        self.__right_rotate(x)
                    x.parent.color = Node.BLACK
                    x.parent.parent.color = Node.RED
                    self.__left_rotate(x.parent.parent)
        self.root.color = Node.BLACK

    def delete(self, z):
        if not z.left or not z.right:
            y = z
        else:
            y = self.successor(z)
        if not y.left:
            x = y.right
        else:
            x = y.left
        x.parent = y.parent

        if not y.parent:
            self.root = x
        else:
            if y == y.parent.left:
                y.parent.left = x
            else:
                y.parent.right = x

        if y != z: z.key = y.key

        if y.color == Node.BLACK:
            self.__delete_fixup(x)

        self.size -= 1
        return y

    def minimum(self, x = None):
        if x is None: x = self.root
        while x.left:
            x = x.left
        return x

    def maximum(self, x = None):
        if x is None: x = self.root
        while x.right:
            x = x.right
        return x

    def successor(self, x):
        if x.right:
            return self.minimum(x.right)
        y = x.parent
        while y and x == y.right:
            x = y
            y = y.parent
        return y

    def predecessor(self, x):
        if x.left:
            return self.maximum(x.left)
        y = x.parent
        while y and x == y.left:
            x = y
            y = y.parent
        return y

    def inorder_walk(self, x = None):
        if x is None: x = self.root
        x = self.minimum()
        while x:
            yield x.key
            x = self.successor(x)

    def reverse_inorder_walk(self, x = None):
        if x is None: x = self.root
        x = self.maximum()
        while x:
            yield x.key
            x = self.predecessor(x)

    def search(self, key, x = None):
        if x is None: x = self.root
        while x and x.key != key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def is_empty(self):
        return bool(self.root)

    def black_height(self, x = None):
        if x is None: x = self.root
        height = 0
        while x:
            x = x.left
            if not x or x.is_black():
                height += 1
        return height

    def __left_rotate(self, x):
        if not x.right:
            raise "x.right is nil!"
        y = x.right
        x.right = y.left
        if y.left: y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.left = x
        x.parent = y

    def __right_rotate(self, x):
        if not x.left:
            raise "x.left is nil!"
        y = x.left
        x.left = y.right
        if y.right: y.right.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.right = x
        x.parent = y

    def __insert_helper(self, z):
        y = NilNode.instance()
        x = self.root
        while x:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        
        z.parent = y
        if not y:
            self.root = z
        else:
            if z.key < y.key:
                y.left = z
            else:
                y.right = z
        

    def __delete_fixup(self, x):
        while x != self.root and x.color == Node.BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == Node.RED:
                    w.color = Node.BLACK
                    x.parent.color = Node.RED
                    self.__left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == Node.BLACK and w.right.color == Node.BLACK:
                    w.color = Node.RED
                    x = x.parent
                else:
                    if w.right.color == Node.BLACK:
                        w.left.color = Node.BLACK
                        w.color = Node.RED
                        self.__right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = Node.BLACK
                    w.right.color = Node.BLACK
                    self.__left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == Node.RED:
                    w.color = Node.BLACK
                    x.parent.color = Node.RED
                    self.__right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == Node.BLACK and w.left.color == Node.BLACK:
                    w.color = Node.RED
                    x = x.parent
                else:
                    if w.left.color == Node.BLACK:
                        w.right.color = Node.BLACK
                        w.color = Node.RED
                        self.__left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = Node.BLACK
                    w.left.color = Node.BLACK
                    self.__right_rotate(x.parent)
                    x = root
        x.color = Node.BLACK


# In[50]:


# check if zip-code is valid
# zipcode has to be 5 digits long, only numeric zipcodes are valid in USA

def is_zip_valid(zipcode):
    
    return (len(zipcode) == 5 and zipcode.isnumeric())


# In[51]:


# check if date is valid
# assumes data has been collected from 2015 to 2017 (present)

def is_date_valid(checkdate):
    
    if len(checkdate) == 8:
        today = str(date.today()).replace('-','')
        
        if today.isnumeric():
            month = int(checkdate[:2])
            day = int(checkdate[2:4])
            year = int(checkdate[4:])
            mon_with_31_days = [1, 3, 5, 7, 8, 10, 12]
            mon_with_30_days = [4, 6, 9, 11]
            
            if (year < 2015 and year > int(today[:4])) or             (month < 1 and month > 12) or             (month == 2 and ((year != 2016 and day == 29) or (day > 28))) or             (day < 1) or             (month in mon_with_31_days and day > 31) or             (month in mon_with_30_days and day > 30): 
                return False
            
            return True
        
    return False


# In[52]:


#f = open("/Users/sangencre/Desktop/NYU/fall_17/Insight_DE_challenge/my_solution/tests/tests/test_1/input/itcont_2.txt")
input_file = open(input_filename, 'r')
output_file_zip = open(output_filename_zip, 'w')
#output_file_date = open(output_filename_date, 'w')
#f_out = open("/Users/sangencre/Desktop/NYU/fall_17/Insight_DE_challenge/my_solution/tests/tests/test_1/input/out_file_zip.txt", "w")

 


# In[53]:


dataframe_dict = {'ID':[], 'Date':[], 'Median':[], 'Number Contributions':[], 'Total':[]}
recipient_info_dict = {} 

# recipient_info_dict = {'id1':[{'zip1': rbt_zip1, 'zip2': rbt_zip2, ...},
#                           {'date1': rbt_date1, 'date2': rbt_date2, ...}], 
#                       'id2':[{'zip1': rbt_zip1, 'zip2': rbt_zip2, ...}, 
#                          {'date1': rbt_date1, 'date2': rbt_date2, ...}], ...other id's}

def create_id_entry(current_id, current_zip, current_date, current_contrib):
    
    if is_zip_valid(current_zip) or is_date_valid(current_date):
        recipient_info_dict[current_id] = []
        rbt = RedBlackTree()
        
        if is_zip_valid(current_zip):
            rbt.add(current_contrib)
            recipient_info_dict[current_id].append({current_zip: copy.deepcopy(rbt)})
            
            write_to_zipcode_file(current_id, 
                              current_zip, 
                              current_contrib, 
                              1, 
                              current_contrib)
            
        else:
            recipient_info_dict[current_id].append({})

        if is_date_valid(current_date):
            rbt = RedBlackTree()
            rbt.add(current_contrib)
            recipient_info_dict[current_id].append({current_date: copy.deepcopy(rbt)})
        else:
            recipient_info_dict[current_id].append({})
        
def create_date_entry(current_id, current_date, current_contrib):    
    if is_date_valid(current_date):
        rbt = RedBlackTree()
        rbt.add(current_contrib)
        recipient_info_dict[current_id][1][current_date] = copy.deepcopy(rbt)
        
def create_zip_entry(current_id, current_zip, current_date, current_contrib):
    if is_zip_valid(current_zip):
        rbt = RedBlackTree()
        rbt.add(current_contrib)
        recipient_info_dict[current_id][0][current_zip] = copy.deepcopy(rbt)
        
        write_to_zipcode_file(current_id, 
                              current_zip, 
                              current_contrib, 
                              1, 
                              current_contrib)

def write_to_zipcode_file(current_id, current_zip, median, num_so_far, total):
#     delim = '|'
    line_to_write = "{0}|{1}|{2}|{3}|{4}|\n".format(current_id, current_zip, median, num_so_far, total)
#     line_to_write = current_id + delim + current_zip + delim + str(median) \
#     + delim + str(num_so_far) + delim + str(total) + '\n'
    output_file_zip.write(line_to_write)





# In[54]:


start=time.time()

#next = f.readline()
next = input_file.readline()
while next != '':
    if next != '\n':
        input_line = next.split('|')
        
        # only consider the record if OTHER_ID is empty, CMTE_ID is non-empty, and TRANSACTION_AMT is non-empty
        if len(input_line) == TOTAL_COLUMNS and input_line[OTHER_ID_index] == ''         and input_line[CMTE_ID_index] != '' and input_line[TRANSACTION_AMT_index] !='':
            
            input_line[-1] = input_line[-1].rstrip() # remove newline character
            input_line_data_list = format_relevant_entries(input_line) # id, zip, date, contribution

            input_line_id = input_line_data_list[0]
            input_line_zip = input_line_data_list[1]
            input_line_date = input_line_data_list[2]
            input_line_contribution = int(input_line_data_list[3])

            
            if input_line_id in recipient_info_dict:
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

for key, dict_list in recipient_info_dict.items():
    for date in dict_list[1]:
        dataframe_dict['ID'].append(key)
        dataframe_dict['Date'].append(format_date(date))
        dataframe_dict['Median'].append(dict_list[1][date].get_median())
        dataframe_dict['Number Contributions'].append(dict_list[1][date].size) 
        dataframe_dict['Total'].append(dict_list[1][date].total)

df = pd.DataFrame(dataframe_dict, columns=['ID','Date','Median','Number Contributions','Total'])

df['Date'] = pd.to_datetime(df.Date)

df.sort_values(by=['ID', 'Date'], inplace=True)

df.to_csv(output_filename_date,
          header=None, index=None, sep='|', date_format='%m%d%Y')

#print(time.time()-start)


# In[43]:


df.head(7)


# In[44]:


# close all files
#f.close()
#f_out.close()
output_file_zip.close()
#output_file_date.close()
input_file.close()


