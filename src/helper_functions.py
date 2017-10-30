from datetime import date



def format_date(date):
    
    formatted = date[:2] + '/' + date[2:4] + '/' + date[4:]
    
    return formatted



# check if zip-code is valid
# zipcode has to be 5 digits long, only numeric zipcodes are valid in USA

def is_zip_valid(zipcode):
    
    return (len(zipcode) == 5 and zipcode.isnumeric())



# check if date is valid
# assumes data has been collected from 2015 to 2017 (present)

def is_date_valid(checkdate):
    
    if len(checkdate) == 8:
        today = str(date.today()).replace('-','')
        
        if checkdate.isnumeric():
            month = int(checkdate[:2])
            day = int(checkdate[2:4])
            year = int(checkdate[4:])
            mon_with_31_days = [1, 3, 5, 7, 8, 10, 12]
            mon_with_30_days = [4, 6, 9, 11]
            year_today = int(today[:4])
            # date is invalid if:
            # 1) year is not in range [2015, now]
            # 2) month is not in the range [1, 12]
            # 3) day is less than 1 for any month
            # 4.a) month is February in any year other than 2016 and day greater than 28
            # 4.b) month is February, year is 2016 and day greater than 29
            # 5) day is greater than 31 for a month with 31 days
            # 6) day is greater than 30 for a month with 30 days
            
            if ((year < 2015 and year > year_today) or (month < 1 and month > 12) or (day < 1) or (month == 2 and ((year != 2016 and day > 28) or (year == 2016 and day > 29))) or (month in mon_with_31_days and day > 31) or (month in mon_with_30_days and day > 30)):
            	return False
            
            return True
        
    return False

