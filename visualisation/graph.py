import h5py
import matplotlib.pyplot as plt
import sys

def gr(filename, var1, var2):
    file = h5py.File(filename, "r+")
    y = file[var1][:,1]
    x = file[var2][:,0]
    if name == "pressure" or "CO2_partial_pressure":
        X = x*1.1574074074074074074074074074074e-5
        Y = y*1e-5
        unit = "bar"
    elif name ==  "temperature":
        X = x*1.1574074074074074074074074074074e-5
        Y = y
        unit = "celsius"
    plt.plot(X, Y, '-')
    plt.title(filename + '/' + var1 + ' vs ' + var2)
    plt.xlabel(var2 + ', day')
    plt.ylabel(var1 + ', ' + unit)
    plt.show()
    return

if __name__=="__main__":
    filename=sys.argv[1]
    var1 = "cell_fields/fluid_" + sys.argv[2]
    var2 = sys.argv[3]
    name = sys.argv[2]
    gr(filename, var1, var2)
