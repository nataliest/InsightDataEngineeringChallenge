This test checks if the irrelevant entries are skipped:
for itcont.txt file
line num	why should skip
line 1		no CMTE_ID 
line 2		OTHER_ID non-empty
line 3		TRANSACTION_AMT empty
line 4		blank line
line 5		extra column(s)
line 6,7 	transaction is invalid (not numeric etc.)
line 8		some random string

the rest is okay.

Output:

medianvals_by_zip.txt
4 entries
medianvals_by_date.txt
4 entries
