#!/usr/bin/python3

"""

Example python script to extract and plot data from the ProcessModel.

Remember to run this model first so you have the Results.sigurd output file!

"""

import matplotlib.pyplot as plt

from volsung.volsungmodel import *

# load the model
model = VolsungModel("Results.sigurd")

wellnames = ["Producer", "Injector"]

# plot reservoir temperature along a well track for both producer and injector
zoneId = -1     # last zone time
f = plt.figure()
ax = plt.subplot(111)
handles = []
for wellname in wellnames:
    well = model.flowNetwork.portObject(wellname)
    # probe the reservoir with the welltrack
    probe = model.reservoir.probeWellTrack(well.wellGridGeometry[zoneId], zoneId, average = True)
    h, = ax.plot(probe["Temperature"] - 273.15, probe["z"], "-")
    handles.append(h)

plt.ylabel("z [m]")
plt.xlabel("Temperature [C]")
plt.legend(handles, wellnames)
plt.title("Reservoir Temperature along Welltrack")

# show the plots
plt.show()
