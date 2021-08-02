#!/usr/bin/python3

"""

Create a TOUGH2 model consisting of two blocks which are equilibrating

"""

from t2data import *
from mulgrids import *
from t2grids import *
import numpy as np


# setup the grid
x = np.array([10.0] * 2)
y = np.array([10.0] * 1)
z = np.array([10.0] * 1)
geo = mulgrid().rectangular(x, y, z)
grid = t2grid().fromgeo(geo)

# name of the single block
block0 = grid.blocklist[0]
block1 = grid.blocklist[1]

# add rock types and material functions
relperm = {'parameters' : [], 'type' : []}
r = rocktype(name = 'ignim', permeability = [1e-15, 20-15, 3e-15], specific_heat = 850, porosity = 1.0)
r.conductivity = 2.0
r.dry_conductivity = r.conductivity
r.capillarity = {'parameters' : [0.0] * 7, 'type' : 8}
r.relative_permeability = {'parameters' : [0.30, 0.05, 0, 0, 0, 0, 0], 'type' : 4}
r.nad = 2 # set this to activate material functions to be written to file
grid.add_rocktype(r)

# set the rock type for the block
block0.rocktype = r
block1.rocktype = r

# create the TOUGH2 input file
data = t2data()
data.grid = grid

# create global material functions for rocks which don't posess any
data.capillarity = r.capillarity
data.relative_permeability = r.relative_permeability

# set the parameter section
data.parameter['gravity'] = 9.81
data.parameter['max_timesteps'] = 100
data.parameter['tstart'] = 0
data.parameter['tstop'] = 100000
data.parameter['const_timestep'] = 10000.0
data.parameter['max_timestep'] =   100000.0
data.parameter['timestep_reduction'] = 2.0
data.parameter['print_interval'] = 1
data.parameter['max_iterations'] = 8
data.parameter['absolute_error'] = 1.0
data.parameter['relative_error'] = 1.0e-5
data.parameter['option'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
data.parameter['default_incons'] = [100e5, 100.0]

# set the print times
data.output_times['time'] = np.arange(10000,100000,10000).tolist()
data.output_times['num_times_specified'] = len(data.output_times['time'])


# set the initial conditions
data.incon[block0.name] = [0, [2e5, 50.0, 0, 0]]
data.incon[block1.name] = [0, [4e5, 100.0, 0, 0]]

# write to file
data.write("T2/RunMe.t2")
data.write("Brynhild/RunMe.t2")
#geo.write("Brynhild/TwoBlocksEquilibrating.dat")
grid = t2grid().fromgeo(geo)
grid.write_vtk(geo, "Brynhild/TwoBlocksEquilibrating.vtu")

