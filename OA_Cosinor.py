# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 22:21:12 2019

@author: Rodrigo
"""

# %% IMPORTATION OF PACKAGES
import csv
import sys
# THESE NEED TO BE INSTALLED
import numpy
import matplotlib.pyplot as plt
import scipy.optimize


# %% FUNCTION DEFINITIONS

def norm(vector):
    """
    A FUNCTION THAT CALCULATES THE EUCLIDEAN NORM OF A vector. THIS EUCLIDEAN
    NORM IS THE SQUARE ROOT OF THE SUM OF THE SQUARES OF EVERY ELEMENT.
    """
    squares = [i**2 for i in vector]
    total = sum(squares)
    return numpy.sqrt(total)

def Aux_Cosinor(params):
    """
    CALCULATES THE COSINOR FUNCTION FOR A GIVEN SET OF data AND THE GIVEN
    coefficients.
    
    THE DATA STRUCTURE IS A MATRIX (OR ANY MATRIX-LIKE ARRAY) WHITH TWO COLUMNS
    ONE FOR TIME VALUES (COLUMN 1) AND THE OTHER FOR MEASUREMENTS (COLUMN 2).
    THE COEFFICIENTS IS AN ARRAY OF THREE ELEMENTS.
    """
    a0, a1, a2 = params
    
    hour = data_struct[:, 0]
    values = data_struct[:, 1]
    values_n = a0 + (a1 * numpy.cos((2 * numpy.pi * (hour - a2)) / 1440))
    values_diff = [values[i] - values_n[i] for i in range(len(values))]
    Ey = norm(values_diff)
    return Ey

def OA_Cosinor(data_struct):
    """
    A FUNCTION THAT CALCULATES THE BEST PARAMETERS TO FIT IN THE COSINOR
    FUNCTION Aux_Cosinor().
    
    REQUIRES ONLY THE DATA STRUCTURE data_struct IN WHICH THE DATA IS STORED.
    IT IS A NUMERICAL ARRAY OF TWO COLUMNS, THE FIRST CONSISTING ON THE
    MEASUREMENT TIMES, AND THE SECOND ON THE MEASURMENTS THEMSELVES.
    """
    values = data_struct[:, 1]
    values_m = sum(values) / len(values)

    initials = [values_m, values_m, 1440/2]
    res = scipy.optimize.minimize(Aux_Cosinor, initials,
                                  method = 'nelder-mead')
    
    a0, a1, a2 = res.x

    return res

def change_time(time_list):
    """
    A FUNCTION THAT CHANGES A TIME VALUE FROM MILITARY TIME (e.g. 0115) TO A
    MINUTE COUNT (0075 IN THIS CASE).
    """
    time_list = [int(time) for time in time_list]
    time_list = ["{:0>4}".format(str(time)) for time in time_list]
    time_list = [int(time[:2]) * 60 + int(time[2:]) for time in time_list]
    return time_list

def read_data(f):
    """
    THIS FUNCTION DETERMINES THE DIALECT (dial) OF A CSV FILE f. I HAVE FOUND
    THAT THE BEST DETERMINATION OF THE DIALECT COMES BY READING ONLY ONE LINE
    OF THE FILE. SO, IN THE LOOP I FIND AT WHICH CHARACTER POSITION THE FIRST
    NEWLINE APPEARS, AND SET THAT POSITION TO DETERMINE THE READING LIMIT FOR
    csv.sniff. THE REST, LIKE ff.seek IS JUST SO THAT THE READING POSITION
    RETURNS TO THE INITIAL POSITION IN THE FILE.
    
    AFTER THE DETERMINATION, THE FILE IS READ AGAIN AND THE DATA IS PASSED TO
    A VARIABLE WHICH CONTAINS IT ALL.
    """
    data = []
    dels = ";\t,"
    sn = csv.Sniffer()
    with open(f, 'r', encoding = 'utf-8-sig') as ff:
        limit = ff.read().find("\n")
        ff.seek(0)
        #header = sn.has_header(ff.read(limit * 5))
        #ff.seek(0)
        dial = sn.sniff(ff.read(limit), delimiters = dels)
        ff.seek(0)
        raw_data = csv.reader(ff, dialect = dial)
        for row in raw_data:
            data.append(row)
        data = numpy.array(data, dtype = float)
        data[:, 0] = change_time(data[:, 0])
    return data


# %% IMPLEMENTATION
finished = False
data = list()
file = sys.argv[1]
data = read_data(file)
#print(data)

out = "Results from analysis of file: {}\n".format(file)
while not finished:
    to_analyze = input("Please enter the columns you would like to analyze, "
                       "separated by commas:\n")
    if to_analyze.lower() == "all":
        total_cols = data.shape[1]
        to_analyze = list(range(1, total_cols))
    else:
        to_analyze = to_analyze.split(",")
        to_analyze = [int(i) for i in to_analyze]
    #print(to_analyze)
    
    for column in to_analyze:
        time = data[:, 0]
        measures = data[:, column]
        data_struct = [[time[i], measures[i]] for i in range(len(time))]
        data_struct = numpy.array(data_struct)
        x = OA_Cosinor(data_struct)
        output = ("Column:\t\t{}\n"
                  "Mesor:\t\t{:.2f} Activity measures\n"
                  "Amplitude:\t{:.2f} Activity measures\n"
                  "Acrophase at \t{}:{:02} hours")
        output = output.format(column, x.x[0], x.x[1], int(x.x[2] / 60), 
                               int(x.x[2] % 60))
        print(output)
        reg = x.x[0] + (x.x[1] * numpy.cos((2 * numpy.pi * (time - x.x[2]))
               / 1440))
        plt.plot(time, measures, '.')
        plt.plot(time, reg)
        plt.xlabel("Time (minutes)")
        plt.ylabel("Measure")
        plt.show()        
        out += "\n" + output + "\n\n" + ("-" * 50)
    
    finish = input("Do you wish to quit? [Y/N]\n")
    finished = finish.lower()[0] == "y"

outfile = input("\nEnter output file:\nIf don't want to save, press 'c'\n"
                "Please avoid using spaces and special characters such as "
                "accents, as these can cause problems in the saving of the "
                "file.\n")
if outfile.lower() != "c":
    print("Data saved to file {}".format(outfile))
    outfile = open(outfile, "w")
    outfile.write(out)
    outfile.close()

goodbyes = ["See you later.", "I hope senpai notices you.",
            "Please use me again.", "Bye :)", "Good day to you too ol' chap."]
print("\n" + goodbyes[numpy.random.randint(0, len(goodbyes) - 1)])
