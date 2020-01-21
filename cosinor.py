# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:59:28 2020

@author: Rodrigo
"""

import numpy
import sys
import reading
import analyze

#%%

file = sys.argv[1]
data = reading.read_file(file)
experiments = numpy.shape(data)[1] - 1
experiments = [None] * experiments
finished = False
#print(Things)
for i in range(len(experiments)):
    ts = analyze.time_series(hour_vector = data[:, 0],
                             measurements = data[:, 1],
                             name = i + 1)
    experiments[i] = ts

while not finished:
    input_query = ("Enter the columns to be analyzed separated by commas:\t")
    while True:
        to_analyze = input(input_query)
        if to_analyze.lower() == "all":
            to_analyze = range(1, len(experiments) + 1)
            break
        elif to_analyze == "-h":
            out = len(experiments)
            print("There are {} columns".format(out))
        else:
            to_analyze = to_analyze.split(",")
            to_analyze = [int(s) for s in to_analyze]
            break
    for column in to_analyze:
        index = column - 1
        experiments[index].cosinor()
        print()
        print(experiments[index])
        experiments[index].compare()
    finish = input("Do yo wish to quit? [y/n]\n")
    if finish.lower() == "y" or finish == "":
        finished = True
    elif finish.lower() == "n":
        finished = False

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
    fitted = [i for i in experiments if i.fitted]
    for series in fitted:
        if series.fitted:
            out_data += str(series) + "\n\n" + "-" * 50 + "\n\n"
    print(out_data)
    out_file = open(out_file, "w")
    out_file.write(out_data)
    out_file.close()

print("The End.")
