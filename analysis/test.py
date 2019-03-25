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
name = "../WorkData/2014-3to5/" + flight
print(name)
data = pre.extract_data(name)
data = pre.nameandtime(data)[1]
basic_data = info.Basic_data(data)
graph.plotaccveldata(data, name, basic_data.landing, basic_data.geardown, basic_data.autopilotoff)

