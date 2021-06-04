import matplotlib.pyplot as plt
import h5py
import numpy as np
import math
import itertools
import sys

def pltheatmap(filename,varname,shape=None):
	infile = h5py.File(filename,"r+")
	n1 = infile[varname][()]
	value = n1[-1,:]
    
	if shape is None:
		w = int(math.sqrt(len(value)))
		h = w
		arr=value.reshape((w,h))
	else: 
		arr=value.reshape(shape)

	plt.imshow(arr, cmap='viridis', origin='lower')
	plt.title(filename+'/'+varname)
	plt.colorbar()
	plt.show()
	return

if __name__=="__main__":
	filename=sys.argv[1]
	varname=sys.argv[2]
	if len(sys.argv) > 3:
		shape = (np.int(sys.argv[3]),np.int(sys.argv[4]))
		pltheatmap(filename,varname,shape)
	else:
		pltheatmap(filename,varname)