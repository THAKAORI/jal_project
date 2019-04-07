import os
import numpy as np
import matplotlib.pyplot as plt
from joblib import Parallel, delayed

import preprocess.data_preprocess as pre
import preprocess.information as info 
import grapher.grapher as graph

rw14r = "/home/takahiro/Confidential/WorkData/2014-3to5/HND RWY34R"
rw15l = "/home/takahiro/Confidential/WorkData/2015-3to5/HND RWY34L"
rw15r = "/home/takahiro/Confidential/WorkData/2015-3to5/HND RWY34R"
rw16l = "/home/takahiro/Confidential/WorkData/2016-3to5/HND RWY34L"
rw16r = "/home/takahiro/Confidential/WorkData/2016-3to5/HND RWY34R"
runwaydir = np.array([[rw14r, "rw14r"], [rw15l, "rw15l"], [rw15r, "rw15r"], [rw16l, "rw16l"], [rw16r, "rw16r"]])

initdir = os.getcwd() 
currentdir = 0
ls = 0
datasize = 0

def landingimpact_investigation(i):
	name = ls[i]
	print(name)
	data = pre.extract_data(currentdir, name)
	data = pre.nameandtime(data)[1]
	intercorporatecolumn = [15, 16, 17, 20, 21]
	data = pre.intercorporate(data,intercorporatecolumn)
	basic_data = info.Basic_data(data, landingdata = True, autopilotdata=True, altitudedata=True, fname = name)
	apoffaltitude = basic_data.autopilotoffalt
	landingimpact = basic_data.landingimpactmax
	return landingimpact, apoffaltitude

def main():
	global currentdir, ls, datasize
	datanum = runwaydir.shape[0]
	for i in range(datanum):
		os.chdir(runwaydir[i, 0])
		currentdir = os.getcwd() 
		print(currentdir)
		ls = os.listdir(currentdir)
		datasize = len(ls)
		result = Parallel(n_jobs=-1)([delayed(landingimpact_investigation)(n) for n in range(datasize)])
		result = np.array(result)

		deletecol = np.empty(0)
		for k in range(result.shape[0]):
			if(result[k,1] < 0 or result[k, 1] > 10000):
				deletecol = np.append(deletecol, k)
			if(result[k, 0] < 1):
				deletecol = np.append(deletecol, k)
		result = np.delete(result, deletecol, 0)
		result = sorted(result, key=lambda x: x[0])
		result = np.array(result)
		graph.scatter_polyfit(result, runwaydir[i, 1], initdir)

main()