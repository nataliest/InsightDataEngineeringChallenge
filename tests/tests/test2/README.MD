This test checks if the irrelevant entries are skipped:
for itcont.txt file
line num	why should skip
line 1		other_id non-empty and zip has less than 5 characters 
line 2		don't skip
line 3		has non-numeric characters
line 4		blank line
line 5		empty column
line 6	 	entry has spaces in addition to numbers
line 7,8,9	has non-numeric characters
line 10 	less than 5 numbers
line 11		is a word


Output:

medianvals_by_zip.txt
1 entry
medianvals_by_date.txt
2 entries (not affected by zipcode, total of 9 contributions for all entries)
