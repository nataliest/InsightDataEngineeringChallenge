'''
    Below are the helper functions that format the data and check for its validity.
    '''

from datetime import date, datetime



def format_date(date):
    formatted = date[:2] + '/' + date[2:4] + '/' + date[4:]
    return formatted


def format_zip(zipcode):
    formatted = zipcode[:5]
    return formatted


# check if zip-code is valid
# zipcode has to be 5 digits long, only numeric zipcodes are valid in USA
def is_zip_valid(zipcode):
    # if provided zip-code has 9 digits, use only the first 5
    form_zip = ''
    if zipcode.isnumeric():
        form_zip = format_zip(zipcode)
    return (len(form_zip) == 5)

# -100, 100 etc. is okay, but 100-, 1abc2, 1.5 etc. is not
def is_amount_valid(check_amount):
    if len(check_amount) > 1:
        return (check_amount[1:].isnumeric() and (check_amount[:1].isnumeric() or check_amount[:1] == '-'))
    else:
        return check_amount.isnumeric()

# check if date is valid
# assumes data has been collected from 2015 to 2017 (present)
def is_date_valid(check_date):
    
    if len(check_date) == 8 and check_date.isnumeric():
        today = str(date.today()).replace('-','')
        month = int(check_date[:2])
        day = int(check_date[2:4])
        year = int(check_date[4:])
        mon_with_31_days = [1, 3, 5, 7, 8, 10, 12]
        mon_with_30_days = [4, 6, 9, 11]
        month_today = int(today[:2])
        day_today = int(today[2:4])
        year_today = int(today[:4])
        # date is invalid if:
        # 1) year is not in range [2015, now]
        # 2) month is not in the range [1, 12]
        # 3) day is less than 1 for any month
        # 4.a) month is February in any year other than 2016 and day greater than 28
        # 4.b) month is February, year is 2016 and day greater than 29
        # 5) day is greater than 31 for a month with 31 days
        # 6) day is greater than 30 for a month with 30 days
        # 7) future date
        
        if ((year < 2015) or (month < 1 or month > 12) or (day < 1) or (month == 2 and ((year != 2016 and day > 28) or (year == 2016 and day > 29))) or (month in mon_with_31_days and day > 31) or (month in mon_with_30_days and day > 30) or (datetime.strptime(check_date + "000000", "%m%d%Y%H%M%S") > datetime.now())):
            return False
            
        return True
        
    return False

