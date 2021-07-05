'''use it like this 
python.exe T_vs_t_plot.py minc_5_spot_250d.h5 temperature pressure 400 (here n is number of elements) 21 (here m is for every diagonal element)
'''

import h5py
import matplotlib.pyplot as plt
import numpy as np
import sys

'''File name'''
out = h5py.File(sys.argv[1])

'''number of elements'''
n=np.int64(sys.argv[4]) 
m=np.int64(sys.argv[5]) #value at every diagonal element

Tv=[268.77, 283.28, 290.75, 294.38, 290.74, 281.84, 261.59, 221.49, 167.41, 127.89, 116.71, 116.06]
Xv=[18.1, 47.63, 101.99, 176.47, 248.75, 318.88, 385.69, 458.49, 527.84, 606.46, 656.23, 686.14]

X=np.linspace(671.65,35.35,20)

y = out['cell_fields/fluid_'+sys.argv[2]][-1,0:n]
Y=y[0::m]

y1 = out['cell_fields/fluid_'+sys.argv[3]][-1,0:n]
Y1=y1[0::m]

fig, ax1=plt.subplots()

ax1.plot(X,Y1,'',label='T')

ax2=ax1.twinx()

ax2.plot(X,Y,'',label='y')

# ax2.plot(Xv,Tv,'',label='T_v')
fig.tight_layout()
plt.legend()
plt.show()
for i in range(0,20):
    print(X[i], Y[i], Y1[i])