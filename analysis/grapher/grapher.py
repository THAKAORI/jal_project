#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 21:49:18 2019

@author: takahiro
"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

def plotaccveldata(datas, name, landing, geardown, autopilotoff):
    plt.figure(figsize=(20,10))
    plt.subplot(5,1,1)
    plt.grid(which='major',color='black',linestyle='-')
    plt.scatter(datas[10000:,0],datas[10000:,3], s = 2,label='alt',color='k')
    #plt.legend()
    ax1 = plt.subplot(5,1,2)
    ax1.scatter(datas[10000:,0],datas[10000:,65-12], s = 2,label='wd',color='red')
    ax2 = ax1.twinx()
    ax2.scatter(datas[10000:,0],datas[10000:,66-12], s = 2,label='ws',color ='c')
    plt.subplot(5,1,3)
    plt.scatter(datas[10000:,0],datas[10000:,41-12], s = 1,label='logg',color='r')
    #plt.legend()
    plt.subplot(5,1,4)
    plt.scatter(datas[10000:,0],datas[10000:,57-12], s = 1,label='logg',color='r')
    plt.scatter(datas[10000:,0],datas[10000:,58-12], s = 1,label='latg',color='b')
    plt.scatter(datas[10000:,0],(datas[10000:,59-12]-1), s = 1,label='vg',color ='g')
    if(geardown < autopilotoff):
        plt.scatter(datas[geardown:,0],(datas[geardown:,59-12]-1), s = 1,label='vg',color ='k')
        plt.scatter(datas[autopilotoff:,0],(datas[autopilotoff:,59-12]-1), s = 1,label='vg',color ='m')
    else:
        plt.scatter(datas[autopilotoff:,0],(datas[autopilotoff:,59-12]-1), s = 1,label='vg',color ='m')
        plt.scatter(datas[geardown:,0],(datas[geardown:,59-12]-1), s = 1,label='vg',color ='k')
    plt.scatter(datas[landing:,0],(datas[landing:,59-12]-1), s = 1,label='vg',color ='y')
    plt.subplot(5,1,5)
    plt.grid(which='major',color='black',linestyle='-')
    plt.scatter(datas[10000:,0],-datas[10000:,30-12], s = 1,label='vv',color='r')
    #plt.legend()
    plt.tight_layout()
    #plt.savefig(name + ".pdf")
    plt.show()

def scatter_polyfit(data, name, datadir):
    pdf = PdfPages(datadir + "/" + name + ".pdf")
    for i in range(1, data.shape[1]):
        plt.figure()
        plt.scatter(data[:,0], data[:,i], s= 5)
        plt.plot(data[:,0], np.poly1d(np.polyfit(data[:,0], data[:,i], 5))(data[:,0]), color = 'red')
        # plt.xlim(0, np.amax(result[:,0]) + 100)
        # plt.ylim(0, np.amax(result[:,1]) + 0.001)
        pdf.savefig()
    pdf.close()
