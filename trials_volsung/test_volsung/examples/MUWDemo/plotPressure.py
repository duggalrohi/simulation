#!/usr/bin/python3

from volsung.volsungmodel import *
import numpy as np
from matplotlib import pyplot as plt

# load the model results
model = VolsungModel("Results.sigurd")

# grab the whole pressure history
# this is indexed by time index, then element index
# note: look up hdf structure and array names using HDFCompass or HDFView
Phist = model.reservoir.history("/reservoir/Elements/Pressure")
# change the index by transposing it, so it is now indexed by element index, then time index
Phist = np.transpose(Phist)

# now locate the cell for which we want to plot the data
# note: we could also look this up in the GUI, but here's the method to do it from a script
pos = (2298735.105848, 5767373.198720, -750.000000)
cellid = model.reservoir.cellId(pos)
# now look up the element index for this cell and MINC layer
elementid = model.reservoir.elementIndex(cellid, 0)

# the pressure history for this cell
P = Phist[elementid]    # pressure in Pa, units are always strict SI

# the times in seconds since 1/1/1970
t = model.reservoir.zoneTimes()
# the times in simple fractional years
ty = model.reservoir.toYearFrac(t)

# plot the pressure over time
plt.figure()
plt.plot(ty, P * 1e-5)              # convert P to bar
plt.ylabel("p [bar]")
plt.show()