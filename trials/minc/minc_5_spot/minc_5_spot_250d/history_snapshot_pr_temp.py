'''usage
python hm.py filename.h5 temperature pressure 400 20 20'''
import h5py as h
import matplotlib.pyplot as plt
import sys
import numpy as np

out=h.File(sys.argv[1])
m='cell_fields/fluid_'+sys.argv[2]
n='cell_fields/fluid_'+sys.argv[3]
p=np.int64(sys.argv[4]) #total number of elements (for minc just the total number of fracture elements)
T1=out[m][-1,0:p]
P1=out[n][-1,0:p]
q=np.int64(sys.argv[5]) #number of x axis grid elements
r=np.int64(sys.argv[6]) #number of y axis grid elements
T=T1.reshape(q,r)
P=P1.reshape(q,r)

gx=out['cell_fields/cell_geometry_centroid'][()]
yms=gx[0:p,0][::q]
xms=gx[0:q,1]

x,y=np.meshgrid(xms,yms)
fig, ax=plt.subplots(1,2,figsize=(16,9))
plt.subplot(1,2,1, autoscale_on=True, aspect='equal')
ax[0]=plt.pcolormesh(x,y,T,cmap='viridis',shading='auto')
plt.colorbar(ax[0],shrink=0.7).set_label('Temperature, $^\circ$C')
plt.subplot(1,2,2, autoscale_on=True, aspect='equal')
ax[1]=plt.pcolormesh(x,y,P*1e-5,cmap='viridis',shading='auto')
plt.colorbar(ax[1],shrink=0.7).set_label('Pressure, bar')
fig.tight_layout()
plt.show()

# out=h.File(sys.argv[1])
# m='cell_fields/fluid_'+sys.argv[2]
# n='cell_fields/fluid_'+sys.argv[3]
# p=np.int64(sys.argv[4]) #total number of elements 
# T1=out[m][-1,0:p]
# P1=out[n][-1,0:p]
# q=np.int64(sys.argv[5]) #number of x axis grid elements
# r=np.int64(sys.argv[6]) #number of y axis grid elements
# T=T1.reshape(q,r)
# P=P1.reshape(q,r)

# l=np.int64(sys.argv[7]) #length of model
# h=np.linspace(0,l,q)
# x,y=np.meshgrid(h,h)

# fig, ax=plt.subplots(1,2)
# fig.add_subplot(1,2,1)
# ax[0]=plt.pcolormesh(x,y,T,cmap='RdBu',shading='auto')
# plt.colorbar(ax[0])
# fig.add_subplot(1,2,2)
# ax[1]=plt.pcolormesh(x,y,P,cmap='RdBu',shading='auto')
# plt.colorbar(ax[1])
# plt.show()