#!/usr/bin/python3

from matplotlib import pyplot as plt

from t2listing import * 
from volsung.volsungmodel import *

title = "Stanford 6"

model = VolsungModel("Brynhild/Results.sigurd", brynhild_fname = "Brynhild/Stanford6.brynhild")     # note: need to explicitly provide brynhild_fname since T2Fafnir does not store xml in results.
elements = model.hdfFile["/zones/zone%d/reservoir/Elements" % (model.reservoir.numberOfZones() - 1)]
x = model.hdfFile["/grid/cells/Centre X"][:]

tough2 = t2listing("T2/TOUGH2.out")                             # results from TOUGH2 in T2 listing file
tough2.set_index(-1)

# find the cell in brynhild output which contains the '  a 5' element in TOUGH2
t2name = '  a 5'
t2sourcename = 'src 1'
cid = model.reservoir.cellId((5.000e+02,4.000e+02,-1.052e+03))
index = numpy.where(elements["Cell Id"][:] == cid)[0][0]        # array index corresponding to the cell id

# plot transients in element
quantities = ["Pressure", "Temperature", "Saturation (gas)"]
for quantity in quantities:
    vals = model.reservoir.history("reservoir/Elements/" + quantity)[:,index]
    # correct the units and grab TOUGH2 data
    if quantity == "Pressure":
        t2time, t2vals = tough2.history([('e', t2name, 'P')])
        vals *= 1e-5
        t2vals *= 1e-5
        ytitle = "p [bar]"
    elif quantity == "Temperature":
        t2time, t2vals = tough2.history([('e', t2name, 'T')])
        vals -= 273.15
        ytitle = "T [$\circ C$]"
    elif quantity == "Saturation (gas)":
        t2time, t2vals = tough2.history([('e', t2name, 'SG')])
        ytitle = "SG"
    plt.figure()
    h1, = plt.plot(model.reservoir.zoneTimes(), vals, 'o b')
    h2, = plt.plot(t2time, t2vals, '+ r')
    plt.xlabel('t [s]')
    plt.ylabel(ytitle)
    plt.legend([h1, h2], ['Volsung', 'TOUGH2'])
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