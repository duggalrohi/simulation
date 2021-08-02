#!/usr/bin/python3

from matplotlib import pyplot as plt

from t2listing import * 
from volsung.volsungmodel import *

title = "Stanford 4"

model = VolsungModel("Brynhild/Results.sigurd", brynhild_fname = "Brynhild/Stanford4.brynhild")     # note: need to explicitly provide brynhild_fname since T2Fafnir does not store xml in results.
elements = model.hdfFile["/zones/zone%d/reservoir/Elements" % (model.reservoir.numberOfZones() - 1)]
z = model.hdfFile["/grid/cells/Centre Z"][:]

tough2 = t2listing("T2/TOUGH2.out")                             # results from TOUGH2 in T2 listing file
tough2.set_index(-1)

# find the cell in brynhild output which contains the '  a20' element in TOUGH2
t2name = '  a20'
t2sourcename = 'src 1'

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
    plt.plot(z, vals, 'o b')
    plt.plot(z, t2vals, '+ r')         # note: this works since elements in TOUGH2 file are ordered in same way as in the volsung model
    plt.xlabel('z [m]')
    plt.ylabel(ytitle)
    plt.title(title)

# plot enthalpy transient in sink    
vals = model.reservoir.history("reservoir/SourcesSinks/Enthalpy")[:,0]
# correct the units and grab TOUGH2 data
t2time, t2vals = tough2.history([('g', (t2name, t2sourcename), 'ENTHALPY')])
vals *= 1e-3
t2vals *= 1e-3
ytitle = "h [kJ/kg]"
plt.figure()
h1, = plt.plot(model.reservoir.zoneTimes(), vals, 'o b')
h2, = plt.plot(t2time, t2vals, '+ r')
plt.xlabel('t [s]')
plt.ylabel(ytitle)
plt.legend([h1, h2], ['Volsung', 'TOUGH2'])
plt.title(title)
    
plt.show()