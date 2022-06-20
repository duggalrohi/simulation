# usage python.exe grid_m_n.py pressure temperature (number of elements along x) (number of elements along y)
# for example a grid which is 4000 m in x and 3500 m in y consists of 90 elements along x and 60 along y due to 50 m blocks
# python.exe grid_m_n.py pressure temperature 90 60


import h5py
import matplotlib.pyplot as plt
import sys
import numpy as np

def gr(filename, var1, var2, Shape=None):
    file = h5py.File(filename, "r+")
    if Shape is None:
        y = file[var1][:,-1] #value of last cell at all simulation times
        x = file[var2][:,0]
        if name == "pressure" or "CO2_partial_pressure":
            X = x*1.1574074074074074074074074074074e-5
            Y = y*1e-5
            unit = "bar"
        elif name ==  "temperature":
            X = x*1.1574074074074074074074074074074e-5
            Y = y
            unit = "celsius"
        else:
            plt.plot(x, y, '-')
            plt.title(filename+'/'+var1+' vs '+ var2)
            plt.show()
        plt.plot(X, Y, '-')
        plt.title(filename + '/' + var1 + ' vs ' + var2)
        plt.xlabel(var2 + ', day')
        plt.ylabel(var1 + ', ' + unit)
        plt.show()
    else:
        val = file[var1][-1,:] #value of all elements at the last simulation time
        arr = val.reshape(Shape)
        plt.imshow(arr, cmap='viridis', origin='lower')
        plt.title(filename+'/'+var1)
        plt.colorbar()
        plt.show()
    return

if __name__=="__main__":
    filename=sys.argv[1]
    var1 = "cell_fields/fluid_" + sys.argv[2]
    var2 = sys.argv[3]
    name = sys.argv[2]
    if len(sys.argv) > 4:
        Shape = (np.int(sys.argv[4]),np.int(sys.argv[5]))
        gr(filename, var1, var2, Shape)
    else:
        gr(filename, var1, var2)
