#!/usr/bin/python3

"""

Create a TOUGH2 model of Stanford Test Problem #1

"""

from t2data import *
from mulgrids import *
from t2grids import *
import numpy as np
import h5py
from matplotlib import pyplot as plt





rate = 10
enthalpy = 678.0566e3


# setup the grid
spacing = 25
r = np.array([spacing] * 40 + [1])

z = np.array([100] * 1)
grid = t2grid().radial(r, z)
N = len(r)

# first and last block
block0 = grid.blocklist[0]
block1 = grid.blocklist[-1]

# add rock types and material functions
relperm = {'parameters' : [], 'type' : []}
r = rocktype(name = 'rock0', permeability = [1e-12, 1e-12, 1e-12], specific_heat = 1000, density = 2500, porosity = 0.2)
r.conductivity = 20
r.dry_conductivity = r.conductivity
r.capillarity = {'parameters' : [0.0] * 7, 'type' : 8}
r.relative_permeability = {'parameters' : [0.30, 0.05, 0, 0, 0, 0, 0], 'type' : 3}
r.nad = 2 # set this to activate material functions to be written to file
grid.add_rocktype(r)

# set the rock type for the blocks
for i in range(N):
    grid.blocklist[i].rocktype = r;

# create the TOUGH2 input file
data = t2data()
data.grid = grid

# create global material functions for rocks which don't posess any
data.capillarity = r.capillarity
data.relative_permeability = r.relative_permeability

# set the parameter section
data.parameter['gravity'] = 9.81
data.parameter['max_timesteps'] = 60
data.parameter['tstart'] = 0
data.parameter['tstop'] = data.parameter['tstart'] + 1e9
data.parameter['const_timestep'] = 1.67e7
data.parameter['max_timestep'] = 1.67e7
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
data.parameter['default_incons'] = [50e5, 170.0]

# set the print times
data.output_times['time'] = (np.arange(0,1e9, 1.67e7)).tolist()
data.output_times['num_times_specified'] = len(data.output_times['time'])


# set the initial conditions
for i in range(N):
    data.incon[grid.blocklist[i].name] = [0, [50e5, 170,0, 0, 0]]

# add source and sink
source = t2generator()
source.name = 'src01'
source.block = block0.name
source.gx = +rate
source.ex = enthalpy
data.add_generator(source)

# Set fixed state
block1.volume = 0   # do not use -ve volumes in pyTough!

# write to file
print("Write to file...")
data.write("T2/RunMe.t2")
print("...done!")


