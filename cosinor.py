# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:59:28 2020

@author: Rodrigo
"""

import pandas as pd
import numpy
import sys
import reading
import analyze

#%% FILE READING AND DATA ORGANIZATION

try:
    file = sys.argv[1]
except:
    file = input("Enter the name of the file you would like to analyze:\n")
data = pd.read_excel(file)
time_header = data.columns[0]
headers = data.columns[1:]
headers = [i for i in headers]
experiments = dict()
data[time_header] = numpy.array([reading.change_time(i)
                                for i in data[time_header]])
finished = False
for name in headers:
    ts = analyze.time_series(hour_vector = data[time_header],
                             measurements = data[name],
                             name = name)
    experiments[name] = ts


#%% DATA ANALYSIS
while not finished:
    input_query = ("Enter the columns to be analyzed separated by commas:\t")
    querying = True
    while querying:
        to_analyze = input(input_query)
        if to_analyze == "-h":
            print(headers)
        elif to_analyze.lower() == "all":
            to_analyze = headers
            querying = False
        else:
            to_analyze = to_analyze.split(",")
            #to_analyze = [i.lower() for i in to_analyze]
            to_analyze = [i.strip() for i in to_analyze]
            if numpy.all(numpy.isin(to_analyze, headers)):
                querying = False
            else:
                error = ("Some of the input columns do not match with the "
                         "column names in the file.")
                print(error)
    for column in to_analyze:
        #index = column - 1
        experiments[column].cosinor()
        print()
        print(experiments[column])
        experiments[column].compare()
    finish = input("Do yo wish to quit? [y/n]\n")
    if finish.lower() == "y" or finish == "":
        finished = True
    elif finish.lower() == "n":
        finished = False

#%% DATA OUTPUT
output_query = input("Do you wish to save the analyzed data? [y/n]\n")
if output_query.lower() == "y":
    out_file = input("Enter the file to which you would like to save. Please "
                     "avoid using special characters such as forward slashes "
                     "(/), back slashes (\\), quotation marks (\") or "
                     "any sort of accent, as they may cause problems while "
                     "saving.\n")
    #print(out_file)
    if len(out_file.split(".")) == 1 or out_file.split(".")[1] != "txt":
        out_file = out_file + ".txt"
    #print(out_file)
    out_data = ""
    fitted = [i for i in experiments if experiments[i].fitted]
    for series in fitted:
        out_data += str(experiments[series]) + "\n\n" + "-" * 50 + "\n\n"
    print(out_data)
    out_file = open(out_file, "w")
    out_file.write(out_data)
    out_file.close()

print("The End.")
