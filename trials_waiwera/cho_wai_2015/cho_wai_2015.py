import h5py as h
import matplotlib.pyplot as plt

file = h.File('cho2015.h5')

Temp = file['cell_fields/fluid_temperature'][:,1769]
time = file['time'][:,0]
for i in range(len(time)):
    print(time[i]*3.17e-8, Temp[i])

plt.plot(time*3.17e-8, Temp, '-')
plt.xlim([0, 40])
plt.ylim([135, 165])
plt.show()