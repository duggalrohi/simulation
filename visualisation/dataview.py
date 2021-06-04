import matplotlib.pyplot as plt
import h5py
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

f = h5py.File('box.h5','r+')
n1 = f['cell_fields/fluid_pressure'][()]
#print(n1[:][:])
cmap = sns.color_palette('Spectral_r', n_colors=20)
plt.figure(figsize = (5, 5))
ax = sns.heatmap(n1, cmap = cmap, linewidth=0)
ax.invert_yaxis()
plt.show()