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
from matplotlib.backends.backend_pdf import PdfPages

import preprocess.data_preprocess as pre
import grapher.grapher as graph
import preprocess.information as info 

initdir = os.getcwd() 
print("first cwd is",initdir)
os.chdir("/home/takahiro/Confidential/WorkData/2015-3to5/HND RWY34L")
currentdir = os.getcwd() 
print(currentdir)
ls = os.listdir(currentdir)
datasize = len(ls)

def main():
	apofftime = np.zeros(datasize)
	apoffverticalgpersec = np.zeros(datasize)
	result = Parallel(n_jobs=-1)([delayed(getapofftime_apoffverticalgpersec)(n) for n in range(datasize)])
	result = np.array(result)

	deletecol = np.empty(0)
	for i in range(result.shape[0]):
		if(result[i,0] < 0):
			deletecol = np.append(deletecol, i)
		elif(result[i,1] > 0.1 or result[i,2] > 0.1):
			deletecol = np.append(deletecol, i)
	result = np.delete(result, deletecol, 0)
	pdf = PdfPages(initdir + "/gtest2015L.pdf")
	plt.figure()
	plt.subplot(3, 1, 1)
	plt.scatter(result[:,0], result[:,1], s= 5)
	plt.xlim(0, np.amax(result[:,0]) + 100)
	plt.ylim(0, np.amax(result[:,1]) + 0.001)
	plt.subplot(3, 1, 2)
	plt.scatter(result[:,0], result[:,2], s= 5)
	plt.xlim(0, np.amax(result[:,0]) + 100)
	plt.ylim(0, np.amax(result[:,2]) + 0.001)
	plt.subplot(3, 1, 3)
	plt.scatter(result[:,0], result[:,3], s= 5)
	plt.xlim(0, np.amax(result[:,0]) + 100)
	plt.ylim(0, np.amax(result[:,3]) + 0.1)
	pdf.savefig()
	plt.figure()
	plt.subplot(3, 1, 1)
	plt.scatter(result[:,0], result[:,4], s= 5)
	plt.xlim(0, np.amax(result[:,0]) + 100)
	plt.ylim(0, np.amax(result[:,4]) + 0.001)
	plt.subplot(3, 1, 2)
	plt.scatter(result[:,0], result[:,5], s= 5)
	plt.xlim(0, np.amax(result[:,0]) + 100)
	plt.ylim(0, np.amax(result[:,5]) + 0.001)
	plt.subplot(3, 1, 3)
	plt.scatter(result[:,0], result[:,6], s= 5)
	plt.xlim(0, np.amax(result[:,0]) + 100)
	plt.ylim(0, np.amax(result[:,6]) + 0.001)
	pdf.savefig()

	pdf.close()

def getapofftime_apoffverticalgpersec(i):
	name = ls[i]
	print(name)
	data = pre.extract_data(name)
	data = pre.nameandtime(data)[1]
	basic_data = info.Basic_data(data)
	apofftime = basic_data.apofftime
	apoffvertical = apoff_verticalg_persecond(data, basic_data.autopilotoff, basic_data.landing)

	return [apofftime, apoffvertical[0], apoffvertical[1], apoffvertical[2], apoffvertical[3], apoffvertical[4], apoffvertical[5]]

def apoff_verticalg_persecond(data, autopilotoff, landing):
	apoffverticalgsum = np.sum(np.square(data[autopilotoff:landing,59-12] - 1))
	apoffverticalgpersec = apoffverticalgsum / (landing - autopilotoff)
	apoffverticaljerksum = 0
	for i in range(autopilotoff,landing-1):
		apoffverticaljerksum += (data[i+1,59-12] - data[i,59-12])**2
	apoffverticaljerkpersec = apoffverticaljerksum / (landing - autopilotoff)

	autopilotong = np.sum(np.square(data[autopilotoff-1000:autopilotoff,59-12] - 1)) / 1000
	apoffperapong = apoffverticalgpersec / autopilotong

	landingfrom1000 = np.sum(np.square(data[landing-1000:landing,59-12] - 1)) / 1000
	landingfrom2000 = np.sum(np.square(data[landing-2000:landing,59-12] - 1)) / 2000
	landingfrom3000 = np.sum(np.square(data[landing-3000:landing,59-12] - 1)) / 3000
	return apoffverticalgpersec ,apoffverticaljerkpersec, apoffperapong, landingfrom1000, landingfrom2000, landingfrom3000


main()
#verticalgtimerelation()