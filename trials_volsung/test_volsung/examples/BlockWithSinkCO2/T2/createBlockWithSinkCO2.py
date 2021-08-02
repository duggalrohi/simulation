#!/usr/bin/python3

"""

Create a TOUGH2 model consisting of one block with a sink attached.

"""

from t2data import *
from mulgrids import *
from t2grids import *
import numpy as np


# setup the grid
x = np.array([1.0] * 1)
y = np.array([1.0] * 1)
z = np.array([1.0] * 1)
geo = mulgrid().rectangular(x, y, z)
grid = t2grid().fromgeo(geo)

# name of the single block
block = grid.blocklist[0]
block_name = grid.blocklist[0].name

# add rock types and material functions
relperm = {'parameters' : [], 'type' : []}
r = rocktype(name = 'ignim', permeability = [1e-15, 2e-15, 3e-15], specific_heat = 850.0, porosity = .05)
r.conductivity = 2.0
r.dry_conductivity = r.conductivity
r.capillarity = {'parameters' : [0.0] * 7, 'type' : 8}
r.relative_permeability = {'parameters' : [0.30, 0.05, 0, 0, 0, 0, 0], 'type' : 4}
r.nad = 2 # set this to activate material functions to be written to file
grid.add_rocktype(r)

# set the rock type for the block
block.rocktype = r

# create the TOUGH2 input file
data = t2data()
data.grid = grid

# set up the solver
data.solver['closure'] = 1e-6
data.solver['relative_max_iterations'] = 0.01
data.solver['type'] = 1

# create global material functions for rocks which don't posess any
data.capillarity = r.capillarity
data.relative_permeability = r.relative_permeability

# set the parameter section
data.parameter['gravity'] = 9.81
data.parameter['max_timesteps'] = 9999
data.parameter['tstart'] = 0
data.parameter['tstop'] = 1000
data.parameter['const_timestep'] = 1.0
data.parameter['max_timestep'] = 10.0
data.parameter['timestep_reduction'] = 2.0
data.parameter['print_interval'] = 1
data.parameter['max_iterations'] = 8
data.parameter['absolute_error'] = 1.0
data.parameter['relative_error'] = 1.0e-5
data.parameter['option'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 3, 0, 3, 0, 0, 7, 0, 0, 0]
data.parameter['default_incons'] = [300e5, 100.0, 10.0e5, 0]

# set the print times
data.output_times['time'] = np.arange(100,1000,100).tolist()
data.output_times['num_times_specified'] = len(data.output_times['time'])


# set the initial conditions
data.incon[block_name] = [0.05, [300e5, 100.0, 10.0e5, 0]]

# create the sink
sink = t2generator()
sink.name = 'snk01'
sink.block = block_name
sink.gx = -.10
data.add_generator(sink)

# write to file
data.write("RunMe.t2")

# write out the grid so we can use it in Brynhild
grid.write_vtk(geo, "SingleBlock.vtu")
