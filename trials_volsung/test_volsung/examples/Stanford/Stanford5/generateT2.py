#!/usr/bin/python3

"""

Create a TOUGH2 model of Stanford Test Problem #5

"""

from t2data import *
from mulgrids import *
from t2grids import *
import numpy as np
import math


# setup the grid
x = np.array([25]*12)
y = np.array([25]*8)
z = np.array([100])
geo = mulgrid().rectangular(x, y, z)
grid = t2grid().fromgeo(geo)




N = 12*8

# first and last block
block0 = grid.blocklist[0]
block1 = grid.blocklist[-1]

# add rock types and material functions
relperm = {'parameters' : [], 'type' : []}
r = rocktype(name = 'rock0', permeability = [25e-15,25e-15, 25e-15], specific_heat = 1000, density = 2500, porosity = 0.35)
r.conductivity = 1
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
data.parameter['max_timesteps'] = 9999
data.parameter['tstart'] = 0
data.parameter['tstop'] = data.parameter['tstart'] + 60*60*24*365*10
data.parameter['const_timestep'] = 60*60*24*100
data.parameter['max_timestep'] = 60*60*24*100
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
data.parameter['default_incons'] = [36e5, 240]

# set the print times
data.output_times['time'] =  (np.arange(0,11,1.0) * 365 * 24 * 60 * 60).tolist()
data.output_times['num_times_specified'] = len(data.output_times['time'])


# set the initial conditions
pressure = 36e5

for i in range(0,N):
    name = grid.blocklist[i].name
    x = grid.block[name].centre[0]
    y = grid.block[name].centre[1]
    if ((x == 62.5) and (y == 62.5)):
        sourcename = name
    r = math.sqrt(x*x + y*y)
    if r <= 100:
        temperature = 240
    elif r >= 300:
        temperature = 160   
    else:
        temperature = (240 - 160 * ((r-100)/200)**2 + 80 * ((r-100)/200)** 4)
        
    #print (name, temperature)
    data.incon[grid.blocklist[i].name] = [0, [pressure, temperature,0, 0, 0]]

# add source and sink
source = t2generator()
source.name = 'src01'
source.block = sourcename
source.gx = -5
source.ex = 0
data.add_generator(source)



# Set fixed state
for i in range(0,N):
    name = grid.blocklist[i].name
    x = grid.block[name].centre[0]
    y = grid.block[name].centre[1]
    if (x == 287.5):
        block = grid.blocklist[i]
        block.volume = 0   # do not use -ve volumes in pyTough!
        grid.demote_block(block.name)

# write to file
print("Write to file...")
data.write("T2/RunMe.t2")
data.write("Brynhild/RunMe.t2")
grid.write_vtk(geo, "Brynhild/Stanford5.vtu")
print("...done!")


