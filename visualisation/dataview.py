import h5py
import sys
import matplotlib.pyplot as plt
import seaborn as sns

def map(filename, varname):
    file = h5py.File(filename, "r+")
    n1 = file[varname][()]
    cmap = sns.color_palette('Spectral_r', n_colors=20)
    plt.figure(figsize = (5, 5))
    ax = sns.heatmap(n1, cmap = cmap, linewidth=0)
    ax.invert_yaxis()
    plt.show()

if __name__=="__main__":
    filename = sys.argv[1]
    varname = "cell_fields/fluid_" + sys.argv[2]
    map(filename, varname)
