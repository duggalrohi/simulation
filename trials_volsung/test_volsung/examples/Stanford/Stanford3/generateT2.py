#!/usr/bin/python3

"""

Create a TOUGH2 model of Stanford Test Problem #3

"""

from t2data import *
from mulgrids import *
from t2grids import *
import numpy as np

# setup the grid
a = np.array([0])
b = np.geomspace(0.16, 2500, 11)
r = np.concatenate((a,b))
x = np.subtract(r[1:11], r[0:10])
y = np.array([20]*1)
z = np.array([0.1]*10)
geo = mulgrid().rectangular(x, y, z)
grid = t2grid().fromgeo(geo)

N = len(x)*len(y)*len(z)

# first and last block
block0 = grid.blocklist[0]
block1 = grid.blocklist[-1]



# add rock types and material functions
relperm = {'parameters' : [], 'type' : []}
r_f = rocktype(name = 'frac0', permeability = [0.3e-12, 0.3e-12, 0.3e-12], specific_heat = 1000, density = 2570, porosity = 0.1)
r_f.conductivity = 0.0
r_f.dry_conductivity = r_f.conductivity
r_f.capillarity = {'parameters' : [0.0] * 7, 'type' : 8}
r_f.relative_permeability = {'parameters' : [0.30, 0.05, 0, 0, 0, 0, 0], 'type' : 3}
r_f.nad = 2 # set this to activate material functions to be written to file
grid.add_rocktype(r_f)

relperm = {'parameters' : [], 'type' : []}
r_b = rocktype(name = 'blck0', permeability = [0.03e-15, 0.03e-15, 0.03e-15], specific_heat = 1000, density = 2570, porosity = 0.1)
r_b.conductivity = 0.0
r_b.dry_conductivity = r_b.conductivity
r_b.capillarity = {'parameters' : [0.0] * 7, 'type' : 8}
r_b.relative_permeability = {'parameters' : [0.30, 0.05, 0, 0, 0, 0, 0], 'type' : 3}
r_b.nad = 2 # set this to activate material functions to be written to file
grid.add_rocktype(r_b)

relperm = {'parameters' : [], 'type' : []}
r_w = rocktype(name = 'well0', permeability = [3e-13, 3e-13, 3e-13], specific_heat = 1000, density = 2570, porosity = 1)
r_w.conductivity = 0.0
r_w.dry_conductivity = r_w.conductivity
r_w.capillarity = {'parameters' : [0.0] * 7, 'type' : 8}
r_w.relative_permeability = {'parameters' : [0.30, 0.05, 0, 0, 0, 0, 0], 'type' : 3}
r_w.nad = 2 # set this to activate material functions to be written to file
grid.add_rocktype(r_w)

relperm = {'parameters' : [], 'type' : []}
r_low = rocktype(name = 'lowp0', permeability = [1e-20, 1e-20, 1e-20], specific_heat = 1000, density = 2570, porosity = 0.1)
r_low.conductivity = 0.0
r_low.dry_conductivity = r_low.conductivity
r_low.capillarity = {'parameters' : [0.0] * 7, 'type' : 8}
r_low.relative_permeability = {'parameters' : [0.30, 0.05, 0, 0, 0, 0, 0], 'type' : 3}
r_low.nad = 2 # set this to activate material functions to be written to file
grid.add_rocktype(r_low)



# create the TOUGH2 input file
data = t2data()
data.grid = grid

# create global material functions for rocks which don't posess any
data.capillarity = r_f.capillarity
data.relative_permeability = r_f.relative_permeability



# set the parameter section
data.parameter['gravity'] = 9.81
data.parameter['max_timesteps'] = 9999
data.parameter['tstart'] = 0
data.parameter['tstop'] = data.parameter['tstart'] + 10000
data.parameter['const_timestep'] = 1
data.parameter['max_timestep'] = 1000
data.parameter['timestep_reduction'] = 4.0
data.parameter['print_interval'] = 1
data.parameter['max_iterations'] = 8
data.parameter['absolute_error'] = 1.0
data.parameter['relative_error'] = 1.0e-5
data.parameter['upstream_weight'] = 1.0
data.parameter['newton_weight'] = 1.0
data.parameter['derivative_increment'] = 0.14901e-7
data.parameter['scale'] = 1.0
data.parameter['option'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 3, 0, 3, 0, 0, 3, 0, 0, 0]  # note: this has a MOP[0], but syntax should use mop 1 as MOP[1]
data.parameter['default_incons'] = [30e5, 0.349880]

# set the print times
data.output_times['time'] = [1,10,1000, 10000]
data.output_times['num_times_specified'] = len(data.output_times['time'])


# set the initial conditions and rock types
for i in range(N):
    name = grid.blocklist[i].name
    x = grid.block[name].centre[0]
    y = grid.block[name].centre[1]
    z = grid.block[name].centre[2]
    if (x< 0.16) and (z < -0.9):
        grid.blocklist[i].rocktype = r_w
    elif (x< 0.16) and (z > -0.9):
        grid.blocklist[i].rocktype = r_low
    elif (x> 0.16) and (z < -0.9):
        grid.blocklist[i].rocktype = r_f
    elif (x> 0.16) and (z > -0.9):
        grid.blocklist[i].rocktype = r_b
    data.incon[grid.blocklist[i].name] = [0, [30.5e5,234,0, 0, 0]]


# add source and sink
source = t2generator()
source.name = 'src01'
source.block = '  a10'
source.gx = -0.028
source.ex = 0
data.add_generator(source)

# Set fixed state
#block1.volume = 0   # do not use -ve volumes in pyTough!

# write to file
print("Write to file...")
data.write("T2/RunMe.t2")
data.write("Brynhild/RunMe.t2")
grid.write_vtk(geo, "Brynhild/Stanford3.vtu")
print("...done!")


