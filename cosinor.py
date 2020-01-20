# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:59:28 2020

@author: Rodrigo
"""

import numpy
import reading
import analyze

#%%

data = reading.read_file("../data.csv")
experiments = numpy.shape(data)[1] - 1
experiments = [None] * experiments
#print(Things)
for i in range(len(experiments)):
    ts = analyze.time_series(hour_vector = data[:, 0],
                                    measurements = data[:, 1])
    experiments[i] = ts
print(experiments)
experiments[0].cosinor()
print(experiments)
