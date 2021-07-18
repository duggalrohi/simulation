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
g=np.int64(sys.argv[4])
n=g*g #number of elements
m=g+1 #value at every diagonal element


'''theory data from 1982-bodvarsson'''
xPLit250d=[18.19, 46.76, 103.24, 174.1, 247.77, 317.48, 384.4, 459.02, 526.97, 604.77, 658.66, 687.55]
PLit250d=[6.14, 6.48, 6.75, 6.93, 7.05, 7.11, 7.25, 7.36, 7.53, 7.83, 8.29, 8.84]
xTLit250d=[19.31, 48.08, 103.96, 175.17, 250.1, 319.98, 384.68, 460.93, 527.44, 605.72, 656.42, 689.1]
TLit250d=[274.89, 269.87, 266.84, 260.57, 250.79, 235.19, 210.57, 184.75, 156.92, 133.72, 121.67, 117.81]

xPLit50d=[17.23, 47.3, 102.73, 174.84, 249.52, 319.22, 386.12, 459.76, 527.68, 606.49, 658.5, 687.11]
PLit50d=[5.53, 6.83, 7.67, 8.03, 8.18, 8.24, 8.36, 8.46, 8.62, 8.94, 9.43, 9.8]
xTLit50d=[18.1, 47.63, 101.99, 176.47, 248.75, 318.88, 385.69, 458.49, 527.84, 606.46, 656.23, 686.14]
TLit50d=[268.77, 283.28, 290.75, 294.38, 290.74, 281.84, 261.59, 221.49, 167.41, 127.89, 116.71, 116.06]

xPsingle=[19.64, 47.97, 104.48, 174.85, 249.53, 319.31, 385.27, 459.82, 529.68, 607.55, 659.56, 687.3]
Psingle=[5.2, 6.64, 7.55, 8.04, 8.19, 8.3, 8.43, 8.5, 8.66, 9, 9.5, 9.92]
xTsingle=[19.89, 47.53, 103.9, 176.46, 248.87, 320, 386.85, 459.61, 526.88, 606.39, 658.17, 686.13]
Tsingle=[264.97, 280.66, 290.16, 294.09, 293.94, 285.63, 266.54, 225.57, 167.42, 126.14, 117, 115.77]

'''waiwera results'''
'''for pressure'''
pr='cell_fields/fluid_'+sys.argv[3]
P1 = out[pr][-1,0:n] 
P=P1[0::m]
'''for temperature'''
temp='cell_fields/fluid_'+sys.argv[2] 
T1=out[temp][-1,0:n] 
T=T1[0::m]

'''method to create x-axis for the plot'''
xdim=out['cell_fields/cell_geometry_centroid'][:,0] #pick x-axis centers of cells
xdim1=xdim[0:n] #value for all elements 
X=xdim1[0::m] #value at every diagonal element
h=[]
for i in range(0,g):
    d=np.sqrt(2)*(X[i]-X[i-1])
    if X[i]:
        d=np.sqrt(2)*X[i]
        h.append(d)
ss=h[::-1] 


fig, ax1=plt.subplots()
ax1.plot(ss,P*1e-6,':',label=pr,color='red')
# ax1.plot(xPLit250d,PLit250d,'-',label='P_lit0250d',color='green')
ax1.plot(xPLit50d,PLit50d,'-',label='P_lit50d',color='green')
ax1.plot(xPsingle,Psingle,'--',label='P_single_lit',color='green')
ax1.set_ylabel('Pressure, MPa')
ax1.set_xlabel('spacing between doublets, m')

ax2=ax1.twinx()

ax2.plot(ss,T,'--',label=temp)
# ax2.plot(xTLit250d,TLit250d,'-',label='T_lit250d')
ax2.plot(xTLit50d,TLit50d,'-',label='T_lit50d')
ax2.plot(xTsingle,Tsingle,'--',label='T_single_lit')
ax2.set_ylabel('Temperature, $^\circ$C')

fig.tight_layout()

ax1.legend(loc='upper center')

plt.legend(loc='lower center')

plt.show()
for i in range(0,20):
    print(ss[i], 1e-6*P[i], T[i])