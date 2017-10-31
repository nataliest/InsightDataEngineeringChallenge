This test checks if the irrelevant entries are skipped:
for itcont.txt file
DATE CHECK
line num	why should skip
line 1		date is empty column 
line 2		Feb 29 2017 is invalid
line 3		has non-numeric characters
line 4		month = 13
line 5		year = 2019 (future year, as of 10/30/2017)
line 6	 	day = 55
line 7		year 2012 is irrelevant, take into account yrs > 2014
line 8		more than 8 characters
line 9		has non-numeric characters
line 10 	less than 8 characters
line 11		April 31 is invalid
line 12		Dec 31 2017 is invalid (future, as of 10/30/2017)

Output:

medianvals_by_zip.txt
15 entries
medianvals_by_date.txt
3 entries for different dates (total of 3 contribuitions)
