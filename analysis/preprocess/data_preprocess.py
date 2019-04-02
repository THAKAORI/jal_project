#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 23:43:12 2019

@author: takahiro
"""

import pandas as pd
import numpy as np
import datetime
import math

def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """
    return np.isnan(y), lambda z: z.nonzero()[0]

def extract_data(data, *, datacutoff = 0):
    data = pd.read_csv(data, header = datacutoff)
    return data.values 

def nameandtime(data):
    for i in range(data.shape[0]):
        if(not(math.isnan(data[i,0]))):
            fnum = int(data[i,0])
            break
    for i in range(data.shape[0]):
        if(type(data[i, 11]) is str):
            firsttimeind = i
            firsttime = data[i, 11]
            firstday = int(data[i, 10])
            firstmonth = int(data[i, 9])
            firstyear = int(data[i, 8])
            break
    firsttime_split = firsttime.split(':')
    firsthour = int(firsttime_split[0])
    firstmin = int(firsttime_split[1])
    firstsec = int(firsttime_split[2])
    if(firstsec == 0):
        firstsec = 59
        if(firstmin == 0):
            firstmin = 59
            firsthour -= 1
        else:
            firstmin -= 1
    else:
        firstsec -= 1
    firstmsec = 1000000 - 125000 * firsttimeind
    firsttimeall = datetime.datetime(firstyear, firstmonth, firstday, firsthour, firstmin, firstsec, firstmsec)
    firstunix = firsttimeall.timestamp()
    step = 0.125
    timearray = np.arange(firstunix, firstunix + data.shape[0] * step, step)
    data = np.delete(data, slice(12), 1)
    timearray = np.reshape(timearray,(timearray.size,1))
    data = np.hstack((timearray, data))
    return fnum ,data
    
def intercorporate(data, intercorporatecolumn):
    for i in intercorporatecolumn:
        y = data[:, i-12].astype('float')
        nans, x= nan_helper(y)
        y[nans]= np.interp(x(nans), x(~nans), y[~nans])
        data[:, i-12] = y.round(2)
    return data