import h5py
import matplotlib.pyplot as plt
import numpy as np

out = h5py.File('minc_5_spot_250d.h5','r+')

T=out['cell_fields/fluid_temperature'][-1,0:400]
T1=T[0::21]

Tv=[268.77, 283.28, 290.75, 294.38, 290.74, 281.84, 261.59, 221.49, 167.41, 127.89, 116.71, 116.06]
Xv=[18.1, 47.63, 101.99, 176.47, 248.75, 318.88, 385.69, 458.49, 527.84, 606.46, 656.23, 686.14]

X=np.linspace(671.65,35.35,20)

P = out['cell_fields/fluid_pressure'][-1,0:400]
P1=P[0::21]

fig, ax1=plt.subplots()

# ax1.plot(X,T1,'',label='T')

ax2=ax1.twinx()

ax2.plot(X,P1*1e-6,'',label='P')

# ax2.plot(Xv,Tv,'',label='T_v')
fig.tight_layout()
plt.legend()
plt.show()
for i in range(0,20):
    print(X[i], P1[i], T1[i])