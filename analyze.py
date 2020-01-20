# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 12:57:56 2020

@author: Rodrigo
"""

import numpy
import scipy.optimize
import random

def norm(vector):
    """
    A FUNCTION THAT CALCULATES THE EUCLIDEAN NORM OF A vector. THIS EUCLIDEAN
    NORM IS THE SQUARE ROOT OF THE SUM OF THE SQUARES OF EVERY ELEMENT.
    
    INPUT
        vector: EITHER A LIST OF NUMBERS OR A ONE-DIMENSIONAL NUMPY ARRAY.
    
    OUTPUT
        n: A FLOAT EQUAL TO THE EUCLIDEAN NORM OF THE INPUT.
    """
    squares = [i**2 for i in vector]
    total = sum(squares)
    n = numpy.sqrt(total)
    return n

def fitting_error(params, time_series):
    """
    CALCULATES THE COSINOR FUNCTION FOR A GIVEN time_series, WITH THE GIVEN
    coefficients. THE COSINOR FUNCTION IS OF THE FORM
        
        a0 + (a1 * numpy.cos((2 * numpy.pi * (hour - a2)) / 1440))
    
    INPUT
        time_series: AN nx2 MATRIX WHOSE FIRST COLUMN REPRESENTS THE TIME AND
        WHOSE SECOND COLUMN REPRESENTS MEASUREMENTS AT SAID TIME.
        
        params: A 1x3 ARRAY OF FLOATS (OR AT LEAST INTEGERS) WITH WHICH THE
        FITTING IS DONE.
    
    OUTPUT
        Ey: A FLOATING POINT VALUE WHICH REPRESENTS THE OVERALL NORM OF THE
        ERROR VECTOR (real_vals - fitted).
    """
    a0, a1, a2 = params
    
    hour = time_series[:, 0]
    real_vals = time_series[:, 1]
    fitted = a0 + (a1 * numpy.cos((2 * numpy.pi * (hour - a2)) / 1440))
    error = [real_vals[i] - fitted[i] for i in range(len(real_vals))]
    Ey = norm(error)
    return Ey

def fitting(time_series):
    """
    CALCULATES AN INITIAL POINT FOR MINIMIZATION OF THE FUNCTION fitting_error
    DEPENDING ON CERTAIN QUALITIES OF THE MEASUREMENTS.
    
    INPUT
        time_series: THE TIMES SERIES WHOSE PARAMETERS WILL BE DETERMINED BY
        THE MINIMIZATION.
    
    OUTPUT
        A LIST OF FLOATS THAT MAKE THE FUNCTION fitting_error MINIMAL.
    """
    hour = time_series[:, 0]
    real_vals = time_series[:, 1]
    values_m = sum(real_vals) / len(real_vals)
    initials = [values_m, values_m, 1440/2]
    res = scipy.optimize.minimize(fitting_error,
                                  x0 = initials,
                                  args = time_series,
                                  method = 'nelder-mead')
    mes, amp, acr = res.x
    if amp < 0:
        amp = numpy.abs(amp)
        acr = acr - 720
    if acr > 1440:
        acr = acr - 1440
    fit = mes + (amp * numpy.cos((2 * numpy.pi * (hour - acr)) / 1440))
    return [mes, amp, acr, fit]


#%%
class time_series():
    """
    A CLASS CONTAINING A TIME SERIES. THIS CLASS WILL ALSO CONTAIN THE
    INFORMATION REGARDING THE COSINOR FIT OF THE TIME SERIES.
    """

    def __init__(self, hour_vector, measurements):
        """
        INITIATES THE CLASS.
        
        INPUT
            hour_vector: A NUMPY ARRAY CONTAINING THE TIME AT WHICH A
            MEASUREMENT WAS MADE.
            
            measurements: A NUMPY ARRAY CONTAINING THE MEASURED DATA.
        """
        self.time = hour_vector
        self.data = measurements
        self.fit = None
        self.mesor = None
        self.amplitude = None
        self.acrophase = None
        self.r2 = None
    
    def __str__(self):
        if not self.fit is None:
            output = ("Mesor:\t\t{:.2f} Activity measures\n"
                      "Amplitude:\t{:.2f} Activity measures\n"
                      "Acrophase at \t{}:{:02} hours\n"
                      "R^2:\t\t{}")
            output = output.format(self.mesor,
                                   self.amplitude,
                                   int(self.acrophase / 60), 
                                   int(self.acrophase % 60),
                                   self.r2)
            return output
        else:
            return "Time series has not been fitted."
    
    def __repr__(self):
        if not self.fit is None:
            output = ("Mesor:\t\t{:.2f} Activity measures\n"
                      "Amplitude:\t{:.2f} Activity measures\n"
                      "Acrophase at \t{}:{:02} hours\n"
                      "R^2:\t\t{}")
            output = output.format(self.mesor,
                                   self.amplitude,
                                   int(self.acrophase / 60), 
                                   int(self.acrophase % 60),
                                   self.r2)
            return output
        else:
            return "Time series has not been fitted."
    
    def cosinor(self):
        r = fitting(numpy.array([self.time, self.data]).T) ### DISLIKE
        self.mesor = r[0]
        self.amplitude = r[1]
        self.acrophase = r[2]
        self.fit = r[3]
        self.r2 = 0.69
        

#%%
if __name__ == "__main__":
    print("CHECK IF norm FUNCTION WORKS PROPERLY.")
    error = "Problems with norm function."
    v = [3, 4]
    assert norm(v) == 5, error
    v = [0, 1]
    assert norm(v) == 1, error
    v = [0, 0, 0, 0, 0]
    assert norm(v) == 0, error
    print("norm FUNCTION WORKS PROPERLY.")

    print("\nCHECK IF fitting_error FUNCTION WORKS PROPERLY.")
    hour = numpy.array([0, 600, 1200, 1800, 2400])
    values = numpy.array([0, 1, 0, -1, 0])
    data = numpy.array([hour, values])
    data = data.T
    #print(data)
    e = fitting_error([0, 2, 3], data)
    print(e)
    print("fitting_error RAISES NO EXCEPTIONS.")

    print("\nCHECK IF fitting FUNCTION WORKS PROPERLY.")
    error = "SOMETHING WRONG WITH fitting."
    for i in range(100):
        h = numpy.linspace(0, 60*24, 25)
        mes, amp, acr = [random.randint(300, 600),
                         random.randint(100, 300),
                         random.randint(0, 1440)]
        d = mes + (amp * numpy.cos((2 * numpy.pi * (h - acr)) / 1440))
        ts = numpy.array([h, d]).T
        r = fitting(numpy.array([h, d]).T)
        e = numpy.array(r[:3]) - numpy.array([mes, amp, acr])
        print(e)
        print(norm(e))
        assert numpy.all(norm(e) < 1e-3), error
    print("fitting WORKS PROPERLY WITHOUT \"NOISE\".")
    
    s = 0.1
    error = "SOMETHING WRONG WITH fitting WITH NOISE."
    for i in range(100):
        h = numpy.linspace(0, 60*24, 25)
        mes, amp, acr = [random.randint(300, 600),
                         random.randint(100, 300),
                         random.randint(0, 1440)]
        d = mes + (amp * numpy.cos((2 * numpy.pi * (h - acr)) / 1440))
        noise = numpy.array([random.gauss(0, s) for i in h])
        d = d + noise
        ts = numpy.array([h, d]).T
        r = fitting(numpy.array([h, d]).T)
        e = numpy.array(r[:3]) - numpy.array([mes, amp, acr])
        print(e)
        assert numpy.all(norm(e) < 1e-3), error
    print("fitting WORKS PROPERLY WITH SMALL \"NOISE\".")
