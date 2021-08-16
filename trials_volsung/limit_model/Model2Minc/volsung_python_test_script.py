#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 08:53:54 2021

@author: jc
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime

import matplotlib.dates as mdates
import vtk
import math
import sys

days = mdates.DayLocator()


from volsung.volsungmodel import *

#Load the model results
model = VolsungModel(sys.argv[1])

# Create a pdf for plots
# now = datetime.datetime.now()
# pdfname = 'DataMatch' + now.strftime("%Y-%m-%d-%H-%M") + '.pdf'
# pdf = PdfPages(pdfname)


zoneId = 1

#List wellnames for plotting here
# wellnames = ['Waihapa-5', 'Ngaere-2']
wellnames = model.flowNetwork.portObjects


##################################################
# plot a temperature slice through the reservoir #
# and display the welltracks on it               #
##################################################

#set elevation for slice
z = -125

f = plt.figure()
ax = plt.subplot(111)                                       # last zone
model.reservoir.slicePlot(f, ax, z, zoneId, arrname = "Temperature", offset = -273.15)
# now print the welltracks onto the plot
model.flowNetwork.plotWellTracks(f, ax, linewidth = 2, color = '#000000', fontsize = 0)
for wellname in wellnames:
    well = model.flowNetwork.portObject('InjectionWell')
    well.plotWellTrackFieldData(f, ax, z, float('nan'), "Temperature", offset = -273.15, radius = 20.0, fontsize = 0, labeloffset = (50, 50))
ax.axis('equal')    # set aspect ratio to equal
plt.title('z = '+ str(z) + 'm')
plt.xticks(rotation=30)
# plt.savefig('slice' + str(z) + '.png', format='png')
# plt.savefig(pdf, format='pdf')
plt.show()
plt.close()



##################################################
# Plot individual temperature matches            #
##################################################

for wellname in wellnames:
    monitor = model.flowNetwork.portObject('Waihapa-5')
    kernel = vtk.vtkShepardKernel() # JC to test difference kernels to decide on default
    kernel.SetNumberOfPoints(6)
    kernel.SetKernelFootprintToNClosest()
    interp = model.reservoir.interpolateWellTrack(monitor.wellGridGeometry[zoneId], zoneId, kernel = kernel)
    probe = model.reservoir.probeWellTrack(monitor.wellGridGeometry[zoneId], zoneId, average = False)   
    ## plot the field data by requiring a time slice.
    ## if time is nan then all data is returned; else data closest to the time provided is chosen
    fielddata = monitor.reservoir1DFieldData.timeSlice(time = float('nan'))
    
    plt.figure()
    plt.plot(interp["Temperature"] - 273.15, interp["z"], '-b')
    plt.plot(probe["Temperature"] - 273.15, probe["z"], '--b')
    plt.plot(fielddata["Temperature"] - 273.15, fielddata["z"], "-r")
    plt.xlim(0,350)
    plt.ylabel("z [m]")
    plt.xlabel("Temperature [C]")
    plt.legend(['Model (Interp)','Model (block)', 'Measured'])
    plt.title(wellname + ' temperature')
    # plt.savefig(pdf, format='pdf')
    # plt.savefig('temperature' + wellname + '.png', format='png')
    plt.show()
    plt.close()
    
##################################################
# Plot well enthalpy over time                   #
##################################################
for well in model.flowNetwork.portObjects:
    if (well.outputPorts[0].fieldHistory("Enthalpy").size  == 0):
        print(well.name + " has no enthalpy data")
    elif (math.isnan(well.outputPorts[0].fieldHistory("Time")[0])):
        print(well.name + " has nan in enthalpy data")
    else:
        f = plt.figure()
        ax = plt.subplot(111)
        h = well.outputPorts[0].zoneHistory("Enthalpy") /1e3
        ax.plot(model.reservoir.toDateTime(model.reservoir.zoneTimes()), h, "o-b")
        ax.plot(model.reservoir.toDateTime(well.outputPorts[0].fieldHistory("Time")), well.outputPorts[0].fieldHistory("Enthalpy")/1e3, "or")
        plt.ylabel("H [kJ/kg]")
        plt.title(well.name)
        plt.legend(['Model', 'Data'], loc = 'best')   
        #ax.xaxis.set_major_locator(days)
        # plt.savefig('Enthalpy' + well.name + '.png', format='png')
        # plt.savefig(pdf, format='pdf')
        plt.show()
        plt.close() 
        
##################################################
# Plot well feedzone pressure over time          #
##################################################
    
f = plt.figure()
ax = plt.subplot(111)
leg = []
for well in model.flowNetwork.portObjects:
    if well.name in wellnames:
        t = model.reservoir.toDateTime(model.reservoir.zoneTimes())
        numzones = len(t)
        fzpressure = []
        for i in range(0, len(t)):
            fzpressure.append(well.feedzoneData(i,'Reservoir Pressure')/1E5)
        ax.plot(t, fzpressure, "o-")              
        elev = well.feedzoneData(0,'Elevation')[0]
        leg.append(well.name + ' at ' + str(elev) + 'm')
ax.set_ylabel("P [bar]")
plt.title('Feedzone Pressures')
plt.legend(leg)
# plt.savefig(pdf, format='pdf') 
plt.show()
plt.close() 



##################################################
# Plot pressure at xyz location over time over   # 
# time with correction for z not at layer centre #
##################################################

#Get pressure history data
Phist = model.reservoir.history("/reservoir/Elements/Pressure")
# change the index by transposing it, so it is now indexed by element index, then time index
Phist = np.transpose(Phist)

#Specify x,y,z position
pos = (x,y,z)
cellid = model.reservoir.cellId(pos)
# now look up the element index for this cell and MINC layer
elementid = model.reservoir.elementIndex(cellid, 0)
# the pressure history for this cell
P = Phist[elementid]    # pressure in Pa, units are always strict SI

adjustment = 0
##Option to adjust pressure based on density if z not at layer centre
#layercentre = model.hdfFile["/grid/cells/Centre Z"][cellid]
#density = model.hdfFile["/zones/zone0/reservoir/Elements/Density (liquid)"][elementid]  
#adjustment = density * 9.81 * (layercentre - elev)

# the times in seconds since 1/1/1970
t = model.reservoir.zoneTimes()
# the times in simple fractional years
ty = model.reservoir.toYearFrac(t)
tdt = model.reservoir.toDateTime(t)

#ax.plot(ty, P * 1e-5, 'b-o', label=wellname)              # convert P to bar   
f = plt.figure()
ax = plt.subplot(111)
ax.plot(ty, (P+adjustment) * 1e-5, 'o-b', label=wellname)              # convert P to bar   
ax.set_ylabel("P [bar]")
plt.title('Plot xyz over time')
# plt.savefig(pdf, format='pdf') 
plt.show()
plt.close() 

# pdf.close()