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
landingclock:unix time
allgeartouch:when all gear is ground

leftgeardown:
rightgeardown:
northgeardown:
geardown:
geardownclock:unix clock
geardowntime:during geardown to landing
geardownalt:altitude

capautopilot:captain autopilot mode change time numpy list
coautopilot:
autopilotoff:when autopilot is off
autopilotoffclock:unix clock
apofftime:during autopilot off to landing
autopilotoffalt:altitude

autothrottle:autothrottle off time
autothrottleoffclock:unix clock

alt1000:altitude 1000ft
alt100:altitude 100ft
"""
import numpy as np

class Basic_data:
    def __init__(self, data, *, landingdata=False, geardowndata=False, autopilotdata=False, autothrottledata=False, altitudedata=False, alldata=False, fname = 'nofile'):
        self.data = data
        if(fname != 'nofile'):
            self.name = fname
        self.datalength = self.data.shape[0]
        if(landingdata or alldata):
            self.getlanding()
            self.firsttouch()
            self.alltouch()
        if(geardowndata or alldata):
            self.getgeardown()
            self.firstgeardown()
        if(autopilotdata or alldata):
            self.autopilot()
            self.apoff()
        if(autothrottledata or alldata):
            self.autothro()
        if(altitudedata or alldata):
            self.altdata()
    def getlanding(self):
        preland = 'GROUND'
        for i in range(self.datalength):
            if(self.data[i,78-12] == 'GROUND' and preland == 'AIR'):
                self.leftlanding = i
                break
            else:
                self.leftlanding = 100000
            if(type(self.data[i,78-12]) == str):
                preland = self.data[i,78-12]
        preland = 'GROUND'
        for i in range(self.datalength):
            if(self.data[i,79-12] == 'GROUND' and preland == 'AIR'):
                self.northlanding = i
                break
            else:
                self.northlanding = 100000
            if(type(self.data[i,78-12]) == str):
                preland = self.data[i,79-12]
        preland = 'GROUND'
        for i in range(self.datalength):
            if(self.data[i,80-12] == 'GROUND' and preland == 'AIR'):
                self.rightlanding = i
                break
            else:
                self.rightlanding = 100000
            if(type(self.data[i,78-12]) == str):
                preland = self.data[i,80-12]
    def firsttouch(self):
        self.landing = min([self.leftlanding,self.northlanding,self.rightlanding])
        self.landingclock = self.data[self.landing, 0]
    def alltouch(self):
        for i in range(self.datalength):
            if(self.data[i,78-12] == 'GROUND' and self.data[i,79-12] == 'GROUND' and self.data[i,80-12] == 'GROUND'):
                self.allgeartouch = i
                break

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
        self.geardownclock = self.data[self.geardown, 0]
        self.geardowntime = self.landingclock - self.geardownclock
        self.geardownalt = self.data[self.geardown, 15 - 12]
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
        self.autothrottleoffclock = self.data[self.autothrottle, 0]
    def apoff(self):
        self.autopilotoff = 0
        for i in range(self.capautopilot.shape[0]):
            if(self.capautopilot[i, 1] == 13 or self.capautopilot[i, 1] == 23):
                self.autopilotoff = int(self.capautopilot[i, 0])
        for i in range(self.coautopilot.shape[0]):
            if(self.coautopilot[i, 1] == 13 or self.coautopilot[i, 1] == 23):
                if(self.coautopilot[i, 0] > self.autopilotoff):
                    self.autopilotoff = int(self.coautopilot[i, 0])
        self.autopilotoffclock = self.data[self.autopilotoff, 0]
        self.apofftime = self.landingclock - self.autopilotoffclock
        self.autopilotoffalt = self.data[self.autopilotoff, 15-12]

    def altdata(self):
        calibrate0alt = self.data[self.allgeartouch,15-12]
        for i in range(self.landing):
            if(self.data[self.landing - i,15-12] - calibrate0alt<=100):
                self.alt100 = self.landing - i
            if(self.data[self.landing - i,15-12] - calibrate0alt<=1000):
                self.alt1000 = self.landing - i
            else:
                break
        self.alt100clock = self.data[self.alt100, 0]
        self.alt1000clock = self.data[self.alt1000, 0]
        self.alt100time = self.landingclock - self.alt100clock
        self.alt1000time = self.landingclock - self.alt1000clock


        