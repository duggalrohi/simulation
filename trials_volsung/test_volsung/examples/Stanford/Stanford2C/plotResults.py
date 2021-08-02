#!/usr/bin/python3

from matplotlib import pyplot as plt

from t2listing import * 
from volsung.volsungmodel import *

title = "Stanford 2C"

model = VolsungModel("Brynhild/Results.sigurd")
elements = model.hdfFile["/zones/zone%d/reservoir/Elements" % (model.reservoir.numberOfZones() - 1)]
x = model.hdfFile["/grid/cells/Centre X"][:]

tough2 = t2listing("T2/TOUGH2.out")                             # results from TOUGH2 in T2 listing file
tough2.set_index(-1)

# plot slices using data from the last time zone
quantities = ["Pressure", "Temperature", "Saturation (gas)"]
for quantity in quantities:
    vals = elements[quantity][:]
    # correct the units and grab TOUGH2 data
    if quantity == "Pressure":
        t2vals = tough2.element["P"]
        vals *= 1e-5
        t2vals *= 1e-5
        ytitle = "p [bar]"
    elif quantity == "Temperature":
        t2vals = tough2.element["T"]
        vals -= 273.15
        ytitle = "T [$\circ C$]"
    elif quantity == "Saturation (gas)":
        t2vals = tough2.element["SG"]
        ytitle = "SG"
    plt.figure()
    h1, = plt.plot(x, vals, 'o b')
    h2, = plt.plot(x, t2vals, '+ r')         # note: this works since elements in TOUGH2 file are ordered in same way as in the volsung model
    plt.xlabel('x [m]')
    plt.ylabel(ytitle)
    plt.legend([h1, h2], ['Volsung', 'TOUGH2'])
    plt.title(title)

# plot transients in third element
for quantity in quantities:
    vals = model.reservoir.history("reservoir/Elements/" + quantity)[:,2]
    # correct the units and grab TOUGH2 data
    if quantity == "Pressure":
        t2time, t2vals = tough2.history([('e', '  c 1', 'P')])
        vals *= 1e-5
        t2vals *= 1e-5
        ytitle = "p [bar]"
    elif quantity == "Temperature":
        t2time, t2vals = tough2.history([('e', '  c 1', 'T')])
        vals -= 273.15
        ytitle = "T [$\circ C$]"
    elif quantity == "Saturation (gas)":
        t2time, t2vals = tough2.history([('e', '  c 1', 'SG')])
        ytitle = "SG"
    plt.figure()
    h1, = plt.plot(model.reservoir.zoneTimes(), vals, 'o b')
    h2, = plt.plot(t2time, t2vals, '+ r')
    plt.xlabel('t [s]')
    plt.ylabel(ytitle)
    plt.legend([h1, h2], ['Volsung', 'TOUGH2'])
    plt.title(title)
    
plt.show()