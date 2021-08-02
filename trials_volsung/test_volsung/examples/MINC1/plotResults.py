#!/usr/bin/python3

from matplotlib import pyplot as plt

from t2listing import * 
from volsung.volsungmodel import *

title = "MINC Model 1"

# make lists to make plotting easier
FS = [50, 300]
model = []
elements = []
tough2 = []
colors_v = ['b', 'c', 'g']
colors_t2= ['r', 'm', 'y']
t2_name = [' kw 1', '2kw 1', '3kw 1']

for fs in FS:
    model_ = VolsungModel("FS%d/Brynhild/Results.sigurd" % fs, brynhild_fname = "FS%d/Brynhild/MINC1_FS%d.brynhild" % (fs, fs))     # note: need to explicitly provide brynhild_fname since T2Fafnir does not store xml in results.
    elements_ = model_.hdfFile["/zones/zone%d/reservoir/Elements" % (model_.reservoir.numberOfZones() - 1)]
    
    tough2_ = t2listing("FS%d/T2/TOUGH2.out" % fs)
    tough2_.set_index(-1)

    model.append(model_)
    elements.append(elements_)
    tough2.append(tough2_)


# plot transients in element
#quantities = ["Pressure", "Temperature", "Saturation (gas)"]
quantities = ["Temperature"]
for i in range(len(FS)):
    for quantity in quantities:
        plt.figure()
        handles = []
        entries = []
        for minc in range(3):
            cid = model[i].reservoir.cellId((1.700e+02,2.500e+02,-5.000e+01))
            index = model[i].reservoir.elementIndex(cid, minc)
        
            vals = model[i].reservoir.history("reservoir/Elements/" + quantity)[:,index]
            # correct the units and grab TOUGH2 data
            if quantity == "Pressure":
                t2time, t2vals = tough2[i].history([('e', t2_name[minc], 'P')])
                vals *= 1e-5
                t2vals *= 1e-5
                ytitle = "p [bar]"
            elif quantity == "Temperature":
                t2time, t2vals = tough2[i].history([('e', t2_name[minc], 'T')])
                vals -= 273.15
                ytitle = "T [$\circ C$]"
            elif quantity == "Saturation (gas)":
                t2time, t2vals = tough2[i].history([('e', t2_name[minc], 'SG')])
                ytitle = "SG"
            h1, = plt.plot(model[i].reservoir.zoneTimes(), vals, 'o ' + colors_v[minc])
            h2, = plt.plot(t2time, t2vals, '+ ' + colors_t2[minc])
            handles.append(h1)
            handles.append(h2)
            entries.append("Volsung #%d" % minc)
            entries.append("TOUGH2 #%d" % minc)
        plt.xlabel('t [s]')
        plt.ylabel(ytitle)
        plt.legend(handles, entries)
        plt.title(title + " - FS = %dm" % FS[i])
    

for i in range(len(FS)):    
    # plot enthalpy transient in sink    
    vals = model[i].reservoir.history("reservoir/SourcesSinks/Enthalpy")[:,0]
    # correct the units and grab TOUGH2 data
    t2time, t2vals = tough2[i].history([('g', (t2_name[0], 'prd 1'), 'ENTHALPY')])
    vals *= 1e-3
    t2vals *= 1e-3
    ytitle = "h [kJ/kg]"
    plt.figure()
    h1, = plt.plot(model[i].reservoir.zoneTimes(), vals, 'o b')
    h2, = plt.plot(t2time, t2vals, '+ r')
    plt.xlabel('t [s]')
    plt.ylabel(ytitle)
    plt.legend([h1, h2], ['Volsung', 'TOUGH2'])
    plt.title(title + " - FS = %dm" % FS[i])
    
plt.show()