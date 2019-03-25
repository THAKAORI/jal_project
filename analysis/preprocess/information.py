#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 21:51:26 2019

@author: takahiro
"""

"""
This class information

leftlanding:when left gear landing
rightlanding:when right gear landing
northlanding
landing:first touch to earth of 3 gears

leftgeardown:
rightgeardown:
northgeardown:
geardown:
geardowntime:during geardown to landing

capautopilot:captain autopilot mode change time numpy list
coautopilot:
autopilotoff:when autopilot is off
apofftime:during autopilot off to landing

autothrottle:autothrottle off time
"""
import numpy as np

class Basic_data:
    def __init__(self, data):
        self.data = data
        self.datalength = self.data.shape[0]
        self.getlanding()
        self.getgeardown()
        self.autopilot()
        self.autothro()
        self.firsttouch()
        self.firstgeardown()
        self.apoff()
    def getlanding(self):
        for i in range(self.datalength):
            if(self.data[i,78-12] == 'GROUND'):
                self.leftlanding = i
                break
        for i in range(self.datalength):
            if(self.data[i,79-12] == 'GROUND'):
                self.northlanding = i
                break
        for i in range(self.datalength):
            if(self.data[i,80-12] == 'GROUND'):
                self.rightlanding = i
                break
    def firsttouch(self):
        self.landing = min([self.leftlanding,self.northlanding,self.rightlanding])
    def getgeardown(self):
        for i in range(self.datalength):
            if(self.data[i,75-12] == 'DN'):
                self.leftgeardown = i
                break
        for i in range(self.datalength):
            if(self.data[i,76-12] == 'DN'):
                self.northgeardown = i
                break
        for i in range(self.datalength):
            if(self.data[i,77-12] == 'DN'):
                self.rightgeardown = i
                break
    def firstgeardown(self):
        self.geardown = min([self.leftgeardown,self.northgeardown,self.rightgeardown])
        self.geardowntime = self.landing - self.geardown
    def autopilot(self):
        self.capautopilot = np.empty((0,2))
        self.coautopilot = np.empty((0,2))
        for i in range(self.datalength):
            if(self.data[i,81-12] == 'OFF' or self.data[i,81-12] == 'CMD' or self.data[i,81-12] == 'CWS'):
                ap_egd_a = self.data[i,81-12]
                ap_egd_b = self.data[i,82-12]
                break
        for i in range(self.datalength):
            if(type(self.data[i,81-12]) == str and self.data[i,81-12] != ap_egd_a):
                if(ap_egd_a == 'CMD'):
                    former = 1
                elif(ap_egd_a == 'CWS'):
                    former = 2
                elif(ap_egd_a == 'OFF'):
                    former = 3
                if(self.data[i,81-12] == 'CMD'):
                    latter = 1
                elif(self.data[i,81-12] == 'CWS'):
                    latter = 2
                elif(self.data[i,81-12] == 'OFF'):
                    latter = 3
                change = former * 10 + latter
                self.capautopilot = np.vstack((self.capautopilot, [i,change]))
                ap_egd_a = self.data[i,81-12]
        for i in range(self.datalength):
            if(type(self.data[i,82-12]) == str and self.data[i,82-12] != ap_egd_b):
                if(ap_egd_b == 'CMD'):
                    former = 1
                elif(ap_egd_b == 'CWS'):
                    former = 2
                elif(ap_egd_b == 'OFF'):
                    former = 3
                if(self.data[i,82-12] == 'CMD'):
                    latter = 1
                elif(self.data[i,82-12] == 'CWS'):
                    latter = 2
                elif(self.data[i,82-12] == 'OFF'):
                    latter = 3
                change = former * 10 + latter
                self.coautopilot = np.vstack((self.coautopilot, [i,change]))
                ap_egd_b = self.data[i,82-12]
    def autothro(self):
        for i in range(self.datalength):
            if(self.data[i,83-12] == 'Not'):
                self.autothrottle = i
    def apoff(self):
        self.autopilotoff = 0
        for i in range(self.capautopilot.shape[0]):
            if(self.capautopilot[i, 1] == 13 or self.capautopilot[i, 1] == 23):
                self.autopilotoff = int(self.capautopilot[i, 0])
        for i in range(self.coautopilot.shape[0]):
            if(self.coautopilot[i, 1] == 13 or self.coautopilot[i, 1] == 23):
                if(self.coautopilot[i, 0] > self.autopilotoff):
                    self.autopilotoff = int(self.coautopilot[i, 0])
        self.apofftime = self.landing - self.autopilotoff
        