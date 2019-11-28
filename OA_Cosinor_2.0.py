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
    
    hour = data[:, 0]
    values = data[:, 1]
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
        header = sn.has_header(ff.read())
        ff.seek(0)
        dial = sn.sniff(ff.read(limit), delimiters = dels)
        ff.seek(0)
        raw_data = csv.reader(ff, dialect = dial)
        for row in raw_data:
            data.append(row)
        data = numpy.array(data, dtype = float)
        data[:, 0] = change_time(data[:, 0])
    return data, header


def analysis(data_matrix, result_dictionary):
    """
    A FUNCTION THAT DOES THE ANALYSIS OF CERTAIN SPECIFIED COLUMNS OF THE
    data_matrix. THESE RESULTS ARE THEN INPUT INTO A result_dictionary WITH THE
    FORMAT:
        r_d = {ID: [MESOR, AMPLITUDE, ACROPHASE]}
    IN WHICH THE ID IS EITHER THE COLUMN NUMBER, OR THE COLUMN NAME (IN FUTURE
    VERSIONS, HOPEFULLY).
    """
    to_analyze = input("Please enter the columns you would like to analyze "
                       "separated by commas:\n")
    if to_analyze.lower() == "all":
        total_cols = data.shape[1]
        to_analyze = list(range(1, total_cols))
    else:
        to_analyze = to_analyze.split(",")
        to_analyze = [int(i) for i in to_analyze]
        
    for column in to_analyze:
        time = data[:, 0]
        measures = data[:, column]
        data_struct = [[time[i], measures[i]] for i in range(len(time))]
        data_struct = numpy.array(data_struct)
        fit = OA_Cosinor(data_struct)
        output = ("Column:\t\t{}\n"
                  "Mesor:\t\t{:.2f} Activity measures\n"
                  "Amplitude:\t{:.2f} Activity measures\n"
                  "Acrophase at \t{}:{:02} hours")
        output = output.format(column, fit.x[0], fit.x[1], int(fit.x[2] / 60), 
                               int(fit.x[2] % 60))
        print(output)
        if column not in result_dictionary.keys():
            result_dictionary[column] = fit

        reg = fit.x[0] + (fit.x[1] * numpy.cos((2 * numpy.pi
                   * (time - fit.x[2])) / 1440))
        plt.plot(time, measures, '.')
        plt.plot(time, reg)
        plt.show()
    return result_dictionary

def compare(data_matrix, result_dictionary):
    """
    THIS FUNCTION PRINTS ANY DESIRED COLUMNS TOGETHER IN ONE GRAPH, IN ORDER TO
    COMPARE THEM. TAKES THE data_matrix TO PLOT THE RAW DATA, AND THE
    result_dictionary TO PLOT THE ADJUSTMENT WITHOUT HAVING TO CALCULATE IT
    ALL OVER AGAIN.
    """
    comparison = input("Which columns would you like to compare?\n")
    comparison = comparison.split(",")
    comparison = [int(i) for i in comparison]
    if not all(column in result_dictionary for column in comparison):
        print("Not all of the desired columns are already analyzed.")
    else:
        print("All are analyzed.")


def say_goodbye():
    """
    JUST A DUMB FUNCTION THAT SAYS GOODBYE IN A RANDOM WAY.
    """
    goodbyes = ["See you later.", "I hope senpai notices you.",
            "Please use me again.", "Bye :)", "Good day to you too ol' chap."]
    print("\n" + goodbyes[numpy.random.randint(0, len(goodbyes) - 1)])

# %% IMPLEMENTATION
analyze_bool = True
compare_bool = False
data = list()
file = sys.argv[1]
data, has_header = read_data(file)
#print(data)
fits = {}

out = "COLMUN ID/NUMBER,MESOR,AMPLITUDE,ACROPHASE\n"
while analyze_bool or compare_bool:
    if analyze_bool:
        analysis(data, fits)
    
    elif compare_bool:
        compare(data, fits)

    query = input("What do you wish to do?\n"
                  "Press '1' to analyze\n"
                  "Press '2' to compare resgressions\n"
                  "Press '3' to quit\n")
    if query == '1':
        analyze_bool = True
        compare_bool = False
    elif query == '2':
        analyze_bool = False
        compare_bool = True
    else:
        analyze_bool = False
        compare_bool = False

outfile = input("\nEnter output file:\nIf don't want to save, press 'c'\n"
                "Please avoid using spaces and special characters such as "
                "accents, as these can cause problems in the saving of the "
                "file.\n")
if outfile.lower() != "c":
    print("Data saved to file {}".format(outfile))
    outfile = open("{}.csv".format(outfile), "w")
    outfile.write("This should work.")
    outfile.close()

say_goodbye()
