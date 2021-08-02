#!/usr/bin/python3

from matplotlib import pyplot as plt

from t2listing import * 
from volsung.volsungmodel import *

title = "Stanford 2B - one node"

model = VolsungModel("Brynhild/Results.sigurd")
elements = model.hdfFile["/zones/zone%d/reservoir/Elements" % (model.reservoir.numberOfZones() - 1)]
x = model.hdfFile["/grid/cells/Centre X"][:]

tough2 = t2listing("T2/TOUGH2.out")                             # results from TOUGH2 in T2 listing file
tough2.set_index(-1)

# plot transients in first element
for quantity in quantities:
    vals = model.reservoir.history("reservoir/Elements/" + quantity)[:,0]
    # correct the units and grab TOUGH2 data
    if quantity == "Pressure":
        t2time, t2vals = tough2.history([('e', '  a 1', 'P')])
        vals *= 1e-5
        t2vals *= 1e-5
        ytitle = "p [bar]"
    elif quantity == "Temperature":
        t2time, t2vals = tough2.history([('e', '  a 1', 'T')])
        vals -= 273.15
        ytitle = "T [$\circ C$]"
    elif quantity == "Saturation (gas)":
        t2time, t2vals = tough2.history([('e', '  a 1', 'SG')])
        ytitle = "SG"
    plt.figure()
    h1, = plt.plot(model.reservoir.zoneTimes(), vals, 'o b')
    h2, = plt.plot(t2time, t2vals, '+ r')
    plt.xlabel('t [s]')
    plt.ylabel(ytitle)
    plt.legend([h1, h2], ['Volsung', 'TOUGH2'])
    plt.title(title)
    
plt.show()