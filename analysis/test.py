#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 17:48:17 2019

@author: takahiro
"""

import preprocess.data_preprocess as pre
import grapher.grapher as graph
import preprocess.information as info 
import sklearn

flight = "HND RWY34L/738-JA306J-20160320-4412270.csv"
name = "/home/takahiro/Confidential/WorkData/2015-3to5/HND RWY34R/738-JA301J-20150301-4011885.csv"
print(name)
data = pre.extract_data(name)
data = pre.nameandtime(data)[1]
intercorporatecolumn = [15]
data = pre.intercorporate(data, intercorporatecolumn)
basic_data = info.Basic_data(data, landingdata = True, geardowndata = True, autopilotdata = True, fname = name)
graph.plotaccveldata(data, name, basic_data.landing, basic_data.geardown, basic_data.autopilotoff)

"""
import numpy as np

def nan_helper(y):

    return np.isnan(y), lambda z: z.nonzero()[0]

y= np.array([1, 1, 1, np.nan, np.nan, 2, 2, np.nan, 0])
nans, x= nan_helper(y)
print(y[~nans])
y[nans]= np.interp(x(nans), x(~nans), y[~nans])
print(y.round(2))

"""
