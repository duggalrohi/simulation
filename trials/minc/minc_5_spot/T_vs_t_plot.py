import h5py
import matplotlib.pyplot as plt
import numpy as np

out = h5py.File('minc_5_spot.h5','r+')

T=out['cell_fields/fluid_temperature'][-1,0:100]
T1=T[0::11]

X=np.linspace(707.1,0,10)
plt.plot(X,T1,'')
plt.show()