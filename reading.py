# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:59:28 2020

@author: Rodrigo
"""

import csv
import numpy

def change_time(millitary_time):
    """
    A FUNCTION THAT CHANGES THE FIRST COLUMN OF A THINGY SO IT IS IN MINUTES
    (MAXIMUM OF 1440) INSTEAD OF HOURS (MAXIMUM OF 2400)
    """
    hours = int(millitary_time / 100) * 60
    #print(hours)
    minutes = ((millitary_time / 100) % 1) * 100
    #print(minutes)
    conversion = int(hours + minutes)
    return conversion

def determine_dialect(file):
    """
    A FUNCTION THAT DETERMINES THE DIALECT OF A .csv FILE SPECIFIED AS ARGUMENT
    AND RETURNS IT FOR A READER FUNCTION TO READ IN THAT DIALECT.
    
    INPUT
        file: CSV FILE
    
    OUTPUT
        A CSV DIALECT CLASS
    """
    file = open(file, "r")
    line = file.readline()
    dialect = csv.Sniffer().sniff(line, delimiters = None)
    file.close()
    return dialect

def read_file(file):
    """
    READS A FILE AND CREATES A TABLE WITH THE CONTENT OF THE FILE. AS THE FILE
    CONTENTS ARE READ AS STRINGS, IT ALSO CHANGES THE CONTENTS TO FLOATING
    POINT VALUES.
    
    INPUT
        file: A CSV FILE CONTAINING DATA. AS OF YET, IT ONLY CONTAINS NUMBERS.
        IN THE FUTURE, IT MIGHT CONTAIN HEADERS TO TELL APPART DIFFERENT
        EXPERIMENTS.
    
    OUTPUT
        A DATA TABLE.
    """
    dialect = determine_dialect(file)
    data = []
    ff = open(file, "r")
    raw_data = csv.reader(ff, dialect = dialect)
    for row in raw_data:
        data.append(row)
    data = numpy.array(data, dtype = float)
    data[:, 0] = [change_time(i) for i in data[:, 0]]
    ff.close()
    return data    


#%%
if __name__ == "__main__":
    print("CHECK IF TIME CHANGING WORKS.")
    error = "Change time works incorrectly."
    assert change_time(0000) == 0, error
    assert change_time(10) == 10, error
    assert change_time(2400) == 1440, error
    assert change_time(542) == 342, error
    assert change_time(1823) == (1440 / 2) + 383
    print("TIME CHANGING WORKS AS IT SHOULD.")
    
    print("\nCHECK IF DIALECT DETERMINATION WORKS.")
    error = "Dialect determination works incorrectly."
    d = determine_dialect("read/sniffer_tabs.csv")
    assert d is not None, error
    d = determine_dialect("read/sniffer_commas.csv")
    assert d is not None, error
    print("DIALECT DETERMINATION WORKS AS IT SHOULD.")
    
    print("\nCHECK IF DATA READING WORKS.")
    error = "Data reading works incorrectly."
    data = read_file("read/reader_tabs.csv")
    assert numpy.shape(data) == (320, 80), error
    data = read_file("read/reader_commas.csv")
    assert numpy.shape(data) == (320, 48), error
    data = read_file("read/reader_semicolon.csv")
    assert numpy.shape(data) == (320, 80), error
    print("DATA READING WORKS AS IT SHOULD.")
