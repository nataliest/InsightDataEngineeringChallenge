# InsightDataEngineeringChallenge
This repository contains my solution for the Insight Data Engineering Fellowship coding challenge.

The description of the challenge can be found here:
https://github.com/InsightDataScience/find-political-donors

My approach to the challenge can be summarized as follows:
- read the input file and write to medianvals_by_zip.txt simultaneously (in the same while loop iteration)
- store and update rolling median and total using RollingMedian class
- before writing to medianvals_by_zip.txt, update the median and the total using RollingMedian objects
- write to medianvals_by_zip.txt
- store and update data for writing to medianvals_by_date.txt
- after reading the file, sort the data using pandas DataFrame object
- write to medianvals_by_date.txt

While processing the data, I am storing the values corresponding to each ID, zip code, and date using Python dictionaries (hash tables). After reading each line (if all relevant fields contain valid data), I update the dictionaries accordingly.

In recipient_info_dict (see code comments for detail), key is the IDs and value is a list of two dictionaries: zip code and date dictionaries.
In zip code dictionaries, keys are the zip codes and values are RollingMedian objects.
In date dictionaries, keys are the dates and values are RollingMedian objects.
Thus, I am calculating medians and keeping track of contributions for every unique zip code and date for each ID.

The dataframe_dict is created in order to place data used for medianvals_by_date.txt in a DataFrame object.

The RollingMedian object calculates rolling medians using min heap and max heap, which is a well-known algorithm for this purpose.

The source code resides in /src/ folder; the folder contains:
1) process_donors_data.py (main program)
2) helper_functions.py
3) rolling_median.py
The latter defines a class called RollingMedian that allows for calculating the rolling median, as well as getting the total amount and the number of contributions streamed so far.

Dependencies and packages:
- pandas: http://pandas.pydata.org/

Running instructions:
- the project was written in Python 3;
- my system has both versions of Python, 2 and 3, therefore my run.sh file explicitly states which version of Python to run, i.e. python3 command
- before running, install pandas (see dependencies above).
Command:
$ python3 ./src/process_donors_data.py ./input/itcont.txt ./output/medianvals_by_zip.txt ./output/medianvals_by_date.txt
Arguments: program source code file, input file, output file (zip codes), output file (dates)

The text processing speed for MacBook Pro (Retina, 13-inch, Early 2013) is ~4.5 MBps.
An 828.8 MB file has been processed in 184.26s.

Input file considerations:
- if zip code is numeric and at least 5 characters, it is considered to be valid; zip codes aren't cross checked with all valid zip code database for a given state;
- the contribution amount is assumed to be an integer; the rounding rules specified in the assignment are being applied ONLY to the median calculations; if the contribution amount is a floating point number, the entry will be considered invalid.

Running the program from the command line will result in two output files:
- medianvals_by_zip.txt: containing a calculated running median, total dollar amount and total number of contributions by recipient and zip code;
- medianvals_by_date.txt: containing the calculated median, total dollar amount and total number of contributions by recipient and date.

Tests:
run_tests.sh DOES NOT run all tests. Instead, each test has its own run.sh script.
