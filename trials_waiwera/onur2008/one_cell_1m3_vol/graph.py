import h5py
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

out = h5py.File(sys.argv[1],"r+")

z = out['cell_fields']['cell_geometry_centroid'][:, 1]

xmin = min(z)-49.9
xmax = max(z)+49.9

ymin = min(z)-49.9
ymax = max(z)+49.9

#T = out['cell_fields/fluid_temperature'][:, 1]
#H = out['source_fields/source_enthalpy'][:, 1]

P = out['cell_fields/fluid_pressure'][:, 0]
time = out['time'][:, 0]
plt.plot(time, P*1e-5, '-')
#plt.xscale('log')
plt.xlabel('')

#plt.plot(time, T, '-')
#plt.ylabel('Enthalpy, kJ')
#plt.xlabel('Temperature')
#plt.ylabel('Temperature')
plt.ylabel('')
#plt.ylim(0,2))
#plt.xlim(0,10)
plt.show()
print(P*1e-5, time)