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

model = VolsungModel(sys.argv[1])
zoneId = 10
wellnames = ['Waihapa-2', 'Ngaere-1', 'Waihapa-6A', 'Waihapa-8', 'Ngaere-2A', 'Ngaere-3', 'Waihapa-4']
z = -180

f = plt.figure()
ax = plt.subplot(111)                                       # last zone
model.reservoir.slicePlot(f, ax, z, zoneId, arrname = "Temperature", offset = -273.15)
#now print the welltracks onto the plot
model.flowNetwork.plotWellTracks(f,ax,linewidth=2,color='#000000',fontsize=0)
for wellname in wellnames:
    well=model.flowNetwork.portObject(wellname)
    well.plotWellTrackFieldData(f,ax,z,float('nan'),"Temperature",offset=-273.15,radius=15,fontsize=10,labeloffset=(10,10))
ax.axis('equal')    # set aspect ratio to equal
plt.xlim((0,3500))
plt.ylim((3500,7500))
plt.xticks(rotation=30)
plt.show()
plt.close()