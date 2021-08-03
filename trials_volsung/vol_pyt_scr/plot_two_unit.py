#!/usr/bin/python3

from matplotlib import pyplot as plt

from t2listing import * 
from volsung.volsungmodel import *

results = VolsungModel("two_unit_model_test.sigurd")

for portobject in results.flowNetwork.portObjects:
    if portobject.name == "prod":
        w = portobject.outputPorts[0].zoneHistory("Mass Rate")

t = results.reservoir.toDateTime(results.reservoir.zoneTimes())

plt.plot(t, w)
plt.show()
print(w)