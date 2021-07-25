'''use it like this 
python.exe T_vs_t_plot.py minc_5_spot_250d.h5 temperature pressure 10 (10*10=100 number of elements of the grid)
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

# xPLit50d=[17.23, 47.3, 102.73, 174.84, 249.52, 319.22, 386.12, 459.76, 527.68, 606.49, 658.5, 687.11]
# PLit50d=[5.53, 6.83, 7.67, 8.03, 8.18, 8.24, 8.36, 8.46, 8.62, 8.94, 9.43, 9.8]
# xTLit50d=[18.1, 47.63, 101.99, 176.47, 248.75, 318.88, 385.69, 458.49, 527.84, 606.46, 656.23, 686.14]
# TLit50d=[268.77, 283.28, 290.75, 294.38, 290.74, 281.84, 261.59, 221.49, 167.41, 127.89, 116.71, 116.06]

# xPsingle=[19.64, 47.97, 104.48, 174.85, 249.53, 319.31, 385.27, 459.82, 529.68, 607.55, 659.56, 687.3]
# Psingle=[5.2, 6.64, 7.55, 8.04, 8.19, 8.3, 8.43, 8.5, 8.66, 9, 9.5, 9.92]
# xTsingle=[19.89, 47.53, 103.9, 176.46, 248.87, 320, 386.85, 459.61, 526.88, 606.39, 658.17, 686.13]
# Tsingle=[264.97, 280.66, 290.16, 294.09, 293.94, 285.63, 266.54, 225.57, 167.42, 126.14, 117, 115.77]

'''TOUGH2 manual results'''
xTOU=[707.1, 636.95568, 565.68, 494.40432, 425.39136, 356.378399999999, 286.23408, 213.82704, 142.55136, 72.4070399999999, 0]
TTOU=[119.587628865979, 124.742268041237, 138.659793814433, 161.340206185567, 189.175257731958, 216.494845360824, 237.628865979381, 255.154639175257, 265.463917525773, 258.247422680412, 206.701030927835]
# xTOU50=[708.23136, 635.82432, 564.54864, 493.27296, 425.39136, 356.378399999999, 283.97136, 213.82704, 143.68272, 71.27568, 1.13135999999997]
# TTOU50=[117.01030927835, 119.587628865979, 133.505154639175, 177.835051546391, 229.381443298969, 263.917525773195, 281.958762886597, 290.20618556701, 291.752577319587, 286.597938144329, 264.432989690721]
# xTOUPM=[707.1, 636.95568, 566.81136, 495.53568, 424.26, 356.378399999999, 283.97136, 212.695679999999, 142.55136, 70.1443199999999, 0]
# TTOUPM=[116.494845360824, 117.525773195876, 130.927835051546, 175.257731958762, 231.958762886597, 268.556701030927, 286.597938144329, 293.298969072164, 293.298969072164, 286.597938144329, 263.917525773195]



'''Volsung'''
xvol=[671.751442127222, 601.040764008566, 530.330085889903, 459.619407771235, 388.90872965255, 318.198051533844, 247.487373415146, 176.776695296493, 106.066017177908, 35.3553390593154]
Pvol=[7.24195, 6.54933, 6.26247, 6.09247, 5.97005, 5.86157, 5.74223, 5.57893, 5.30587, 3.39358]
xTvol=[671.751442127222, 601.040764008566, 530.330085889903, 459.619407771235, 388.90872965255, 318.198051533844, 247.487373415146, 176.776695296493, 106.066017177908, 35.3553390593154]
Tvol=[121.094, 135.282, 158.348, 186.521, 214.029, 236.412, 252.417, 263.378, 267.68, 240.793]

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
ax1.plot(ss,P*1e-6,'-',label='waiwera_'+pr,color='red')
ax1.plot(xPLit250d,PLit250d,':',label='1982_bodvarsson_case_P',color='green')
# ax1.plot(xPLit50d,PLit50d,'v',label='P_lit50d',color='green')
# ax1.plot(xPsingle,Psingle,'1',label='P_single_lit',color='green')
ax1.plot(xvol,Pvol,'s',label='Volsung_results_P',color='black')
ax1.set_ylabel('Pressure, MPa')
ax1.set_xlabel('spacing between doublets, m')

ax2=ax1.twinx()

ax2.plot(ss,T,'-',label='waiwera_'+temp,color='red')
ax2.plot(xTLit250d,TLit250d,':',label='1982_bodvarsson_case_T',color='green')
# ax2.plot(xTLit50d,TLit50d,'s',label='T_lit50d')
# ax2.plot(xTsingle,Tsingle,'p',label='T_single_lit')
ax2.plot(xTOU,TTOU,'--',label='Tough2_manual_results_T')
# ax2.plot(xTOU50,TTOU50,'*',label='T_TOUGH50m')
# ax2.plot(xTOUPM,TTOUPM,'+',label='T_TOUGH_porousM')
ax2.plot(xTvol,Tvol,'s',label='Volsung_results_T', color='black')
ax2.set_ylabel('Temperature, $^\circ$C')

fig.tight_layout()

ax1.legend(loc='upper right')

plt.legend(loc='lower right')

plt.show()
for i in range(0,g):
    print(ss[i], 1e-6*P[i], T[i])