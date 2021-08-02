#!/usr/bin/python3

from matplotlib import pyplot as plt

from t2listing import * 
from volsung.volsungmodel import *

title = "Two Blocks Equilibrating"

model = VolsungModel("Brynhild/Results.sigurd", brynhild_fname = "Brynhild/TwoBlocksEquilibrating.brynhild")
elements = model.hdfFile["/zones/zone%d/reservoir/Elements" % (model.reservoir.numberOfZones() - 1)]
x = model.hdfFile["/grid/cells/Centre X"][:]

tough2 = t2listing("T2/TOUGH2.out")                             # results from TOUGH2 in T2 listing file
tough2.set_index(-1)

# plot transients in elements
t2blocks = ['  a 1', '  b 1']
quantities = ["Pressure", "Temperature"]
for i in range(2):
    for quantity in quantities:
        plt.figure()
        vals = model.reservoir.history("reservoir/Elements/" + quantity)[:,i]
        # correct the units and grab TOUGH2 data
        if quantity == "Pressure":
            t2time, t2vals = tough2.history([('e', t2blocks[i], 'P')])
            vals *= 1e-5
            t2vals *= 1e-5
            ytitle = "p [bar]"
        elif quantity == "Temperature":
            t2time, t2vals = tough2.history([('e', t2blocks[i], 'T')])
            vals -= 273.15
            ytitle = "T [$\circ C$]"
        elif quantity == "Saturation (gas)":
            t2time, t2vals = tough2.history([('e', t2blocks[i], 'SG')])
            ytitle = "SG"
        plt.plot(model.reservoir.zoneTimes(), vals, 'o b')
        plt.plot(t2time, t2vals, '+ r')
        plt.xlabel('t [s]')
        plt.ylabel(ytitle)
        plt.title(title + " - Block %d" % i)
    
plt.show()