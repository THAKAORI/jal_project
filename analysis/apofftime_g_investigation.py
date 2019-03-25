#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 17:48:17 2019

@author: takahiro
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from joblib import Parallel, delayed

import preprocess.data_preprocess as pre
import grapher.grapher as graph
import preprocess.information as info 

initdir = os.getcwd() 
print("first cwd is",initdir)
os.chdir("/home/takahiro/Confidential/WorkData/2014-3to5/HND RWY34L")
currentdir = os.getcwd() 
print(currentdir)
ls = os.listdir(currentdir)
datasize = len(ls)

def main():
	apofftime = np.zeros(datasize)
	apoffverticalgpersec = np.zeros(datasize)
	result = Parallel(n_jobs=-1)([delayed(getapofftime_apoffverticalgpersec)(n) for n in range(datasize)])
	result = np.array(result)
	plt.scatter(result[:,0], result[:,1])
	plt.savefig(initdir + "/gtest.pdf")
	plt.show()

def getapofftime_apoffverticalgpersec(i):
	name = ls[i]
	print(name)
	data = pre.extract_data(name)
	data = pre.nameandtime(data)[1]
	basic_data = info.Basic_data(data)
	apofftime = basic_data.apofftime
	apoffverticalgpersec = apoff_verticalg_persecond(data, basic_data.autopilotoff, basic_data.landing)

	return [apofftime, apoffverticalgpersec]

def apoff_verticalg_persecond(data, autopilotoff, landing):
	apoffverticalgsum = np.sum(np.square(data[autopilotoff:landing,59-12] - 1))
	apoffverticalgpersec = apoffverticalgsum / (landing - autopilotoff)

	return apoffverticalgpersec

main()