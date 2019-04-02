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
os.chdir("/home/takahiro/Confidential/WorkData/2016-3to5/HND RWY34R")
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
		if(result[i,0] < 0 or result[i, 0] > 10000):
			deletecol = np.append(deletecol, i)
		elif(result[i,1] > 0.1 or result[i,2] > 0.1):
			deletecol = np.append(deletecol, i)
	result = np.delete(result, deletecol, 0)
	result = sorted(result, key=lambda x: x[0])
	result = np.array(result)


	pdf = PdfPages(initdir + "/gtest2016R.pdf")
	plt.figure()
	plt.scatter(result[:,0], result[:,1], s= 5, label = "ver g per sec")
	plt.plot(result[:,0], np.poly1d(np.polyfit(result[:,0], result[:,1], 5))(result[:,0]), color = 'red')
	plt.xlim(0, np.amax(result[:,0]) + 100)
	plt.ylim(0, np.amax(result[:,1]) + 0.001)
	plt.legend()
	pdf.savefig()
	plt.figure()
	plt.scatter(result[:,0], result[:,2], s= 5, label = "ver jerk per sec")
	plt.plot(result[:,0], np.poly1d(np.polyfit(result[:,0], result[:,2], 5))(result[:,0]), color = 'red')
	plt.xlim(0, np.amax(result[:,0]) + 100)
	plt.ylim(0, np.amax(result[:,2]) + 0.001)
	plt.legend()
	pdf.savefig()
	plt.figure()
	plt.scatter(result[:,0], result[:,3], s= 5, label = "ver apoff apon g ratio")
	plt.plot(result[:,0], np.poly1d(np.polyfit(result[:,0], result[:,3], 5))(result[:,0]), color = 'red')
	plt.xlim(0, np.amax(result[:,0]) + 100)
	plt.ylim(0, np.amax(result[:,3]) + 0.1)
	plt.legend()
	pdf.savefig()
	plt.figure()
	plt.scatter(result[:,0], result[:,4], s= 5, label = "15sec g from flare")
	plt.plot(result[:,0], np.poly1d(np.polyfit(result[:,0], result[:,4], 5))(result[:,0]), color = 'red')
	plt.xlim(0, np.amax(result[:,0]) + 100)
	plt.ylim(0, np.amax(result[:,4]) + 0.001)
	plt.legend()
	pdf.savefig()
	plt.figure()
	plt.scatter(result[:,0], result[:,5], s= 5, label = "60sec g from flare")
	plt.plot(result[:,0], np.poly1d(np.polyfit(result[:,0], result[:,5], 5))(result[:,0]), color = 'red')
	plt.xlim(0, np.amax(result[:,0]) + 100)
	plt.ylim(0, np.amax(result[:,5]) + 0.001)
	plt.legend()
	pdf.savefig()
	plt.figure()
	plt.scatter(result[:,0], result[:,6], s= 5, label = "180sec g from flare")
	plt.plot(result[:,0], np.poly1d(np.polyfit(result[:,0], result[:,6], 5))(result[:,0]), color = 'red')
	plt.xlim(0, np.amax(result[:,0]) + 100)
	plt.ylim(0, np.amax(result[:,6]) + 0.001)
	plt.legend()
	pdf.savefig()
	plt.figure()
	plt.scatter(result[:,0], result[:,7], s= 5, label = "wind")
	plt.plot(result[:,0], np.poly1d(np.polyfit(result[:,0], result[:,7], 5))(result[:,0]), color = 'red')
	plt.xlim(0, np.amax(result[:,0]) + 100)
	plt.ylim(0, np.amax(result[:,7]) + 0.1)
	plt.legend()
	pdf.savefig()


	pdf.close()

def getapofftime_apoffverticalgpersec(i):
	name = ls[i]
	print(name)
	data = pre.extract_data(name)
	data = pre.nameandtime(data)[1]
	intercorporatecolumn = [15, 16, 17, 20, 21]
	data = pre.intercorporate(data,intercorporatecolumn)
	basic_data = info.Basic_data(data, alldata = True, fname = name)
	apofftime = basic_data.apofftime
	apoffvertical = apoff_verticalg_persecond_noflare(data, basic_data)
	apoffaltitude = basic_data.autopilotoffalt

	return [apoffaltitude, apoffvertical[0], apoffvertical[1], apoffvertical[2], apoffvertical[3], apoffvertical[4], apoffvertical[5], apoffvertical[6]]

def apoff_verticalg_persecond(data, basic_data):
	apoffverticalgsum = np.sum(np.square(data[basic_data.autopilotoff:basic_data.landing,59-12] - 1))
	apoffverticalgpersec = apoffverticalgsum / basic_data.apofftime
	apoffverticaljerksum = 0
	for i in range(basic_data.autopilotoff,basic_data.landing-1):
		apoffverticaljerksum += (data[i+1,59-12] - data[i,59-12])**2
	apoffverticaljerkpersec = apoffverticaljerksum / basic_data.apofftime
	if(basic_data.autopilotoff >= 800):
		autopilotong = np.sum(np.square(data[basic_data.autopilotoff-800:basic_data.autopilotoff,59-12] - 1)) / 100
	else:
		autopilotong = np.sum(np.square(data[basic_data.autopilotoff-80:basic_data.autopilotoff,59-12] - 1)) / 10
	if(autopilotong == 0):
		apoffperapong = 0
		apoffverticalgpersec = 100
	else:
		apoffperapong = apoffverticalgpersec / autopilotong

	landingfrom60 = np.sum(np.square(data[basic_data.landing-480:basic_data.landing,59-12] - 1)) / 60
	landingfrom180 = np.sum(np.square(data[basic_data.landing-1440:basic_data.landing,59-12] - 1)) / 180
	landingfrom1000 = np.sum(np.square(data[basic_data.landing-8000:basic_data.landing,59-12] - 1)) / 1000

	windaverage = np.nansum(data[basic_data.autopilotoff:basic_data.landing,66-12]) / basic_data.apofftime
	#print(windaverage)
	return apoffverticalgpersec ,apoffverticaljerkpersec, apoffperapong, landingfrom15, landingfrom60, landingfrom180, windaverage

def apoff_verticalg_persecond_noflare(data, basic_data):
	apoffverticalgsum = np.sum(np.square(data[basic_data.autopilotoff:basic_data.alt100,59-12] - 1))
	apoffverticalgpersec = apoffverticalgsum / (basic_data.apofftime - basic_data.alt100time)
	apoffverticaljerksum = 0
	for i in range(basic_data.autopilotoff,basic_data.alt100-1):
		apoffverticaljerksum += (data[i+1,59-12] - data[i,59-12])**2
	apoffverticaljerkpersec = apoffverticaljerksum / (basic_data.apofftime - basic_data.alt100time)
	if(basic_data.autopilotoff >= 800):
		autopilotong = np.sum(np.square(data[basic_data.autopilotoff-800:basic_data.autopilotoff,59-12] - 1)) / 100
	else:
		autopilotong = np.sum(np.square(data[basic_data.autopilotoff-80:basic_data.autopilotoff,59-12] - 1)) / 10
	if(autopilotong == 0):
		apoffperapong = 0
		apoffverticalgpersec = 100
	else:
		apoffperapong = apoffverticalgpersec / autopilotong

	landingfrom15 = np.sum(np.square(data[basic_data.alt100-120:basic_data.alt100,59-12] - 1)) / 15
	landingfrom60 = np.sum(np.square(data[basic_data.alt100-480:basic_data.alt100,59-12] - 1)) / 60
	landingfrom180 = np.sum(np.square(data[basic_data.alt100-1440:basic_data.alt100,59-12] - 1)) / 180

	windaverage = np.nansum(data[basic_data.autopilotoff:basic_data.landing,66-12]) / basic_data.apofftime
	#print(windaverage)
	return apoffverticalgpersec ,apoffverticaljerkpersec, apoffperapong, landingfrom15, landingfrom60, landingfrom180, windaverage


main()
#verticalgtimerelation()