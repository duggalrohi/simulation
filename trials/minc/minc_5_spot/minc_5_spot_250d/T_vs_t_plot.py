'''use it like this 
python.exe T_vs_t_plot.py minc_5_spot_250d.h5 temperature pressure 400 (here n is number of elements) 21 (here m is for every diagonal element)
'''

import h5py
import matplotlib.pyplot as plt
import numpy as np
import sys
import math

'''File name'''
out = h5py.File(sys.argv[1])

'''number of elements'''
n=np.int64(sys.argv[4]) 
m=np.int64(sys.argv[5]) #value at every diagonal element


'''theory data from 1982-bodvarsson'''
xLit250d=[18.19, 46.76, 103.24, 174.1, 247.77, 317.48, 384.4, 459.02, 526.97, 604.77, 658.66, 687.55]
PLit250d=[6.14, 6.48, 6.75, 6.93, 7.05, 7.11, 7.25, 7.36, 7.53, 7.83, 8.29, 8.84]
xTLit250d=[19.31, 48.08, 103.96, 175.17, 250.1, 319.98, 384.68, 460.93, 527.44, 605.72, 656.42, 689.1]
TLit250d=[274.89, 269.87, 266.84, 260.57, 250.79, 235.19, 210.57, 184.75, 156.92, 133.72, 121.67, 117.81]



'''waiwera results'''
'''for pressure'''
P1 = out['cell_fields/fluid_'+sys.argv[2]][-1,0:n] 
P=P1[0::m]
'''for temperature''' 
T1=out['cell_fields/fluid_'+sys.argv[3]][-1,0:n] 
T=T1[0::m]

'''method to create x-axis for the plot'''
xdim=500 #model dimension e.g., here is 500 by 500
div=2*(m-1) #just a variable to get the location of first cell center
b=np.sqrt(2) * (xdim/div) #diagonal distance of first cell center
c=(np.sqrt(2) * xdim) - b #diagonal distance between cell centers of last and first cells
X=np.linspace(c,b,len(P)) #divisions created to plot Pressure or Temperature 


fig, ax1=plt.subplots()
ax1.plot(X,P*1e-6,'',label='P'+sys.argv[2])

ax2=ax1.twinx()
# ax3=ax1.twinx()
ax2.plot(xLit250d,PLit250d,'',label='theory')
# ax3.plot(X,T,'',label=sys.argv[3])


fig.tight_layout()
plt.legend()
plt.show()
for i in range(0,20):
    print(X[i], P[i], T[i])