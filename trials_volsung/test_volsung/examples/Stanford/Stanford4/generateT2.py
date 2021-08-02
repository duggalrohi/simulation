#!/usr/bin/python3

"""

Create a TOUGH2 model of Stanford Test Problem #4

"""

from t2data import *
from mulgrids import *
from t2grids import *
from IAPWS97 import *
import numpy as np

rate = 100
enthalpy = 1025.830000e3


# setup the grid

x = np.array([1000])
y = np.array([1000])
z = np.array([100] * 20)
geo = mulgrid().rectangular(x, y, z)
grid = t2grid().fromgeo(geo)
grid.write_vtk(geo, "Brynhild/Stanford4.vtu")


N = 20

# first and last block
block0 = grid.blocklist[0]
block1 = grid.blocklist[-1]

# add rock types and material functions
relperm = {'parameters' : [], 'type' : []}
r = rocktype(name = 'rock0', permeability = [100e-15,100e-15, 100e-15], specific_heat = 1000, density = 2500, porosity = 0.25)
r.conductivity = 1
r.dry_conductivity = r.conductivity
r.capillarity = {'parameters' : [0.0] * 7, 'type' : 8}
r.relative_permeability = {'parameters' : [0.30, 0.05, 0, 0, 0, 0, 0], 'type' : 3}
r.nad = 2 # set this to activate material functions to be written to file
grid.add_rocktype(r)

relperm = {'parameters' : [], 'type' : []}
r1 = rocktype(name = 'rock1', permeability = [5e-15, 5e-15, 5e-15], specific_heat = 1000, density = 2500, porosity = 0.15)
r1.conductivity = 1
r1.dry_conductivity = r.conductivity
r1.capillarity = {'parameters' : [0.0] * 7, 'type' : 8}
r1.relative_permeability = {'parameters' : [0.30, 0.05, 0, 0, 0, 0, 0], 'type' : 3}
r1.nad = 2 # set this to activate material functions to be written to file
grid.add_rocktype(r1)


# set the rock type for the blocks
for i in range(N):
    if i < 10:
        grid.blocklist[i].rocktype = r1;
    else:
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
data.parameter['tstop'] = data.parameter['tstart'] + 60*60*24*365*40
data.parameter['const_timestep'] = 60*60*24*365
data.parameter['max_timestep'] = 60*60*24*365
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
data.output_times['time'] =  (np.arange(0,41,1.0) * 365 * 24 * 60 * 60).tolist()
data.output_times['num_times_specified'] = len(data.output_times['time'])


# set the initial conditions
p_last = 1.013e5 #Hydrostatis pressure at 50m if 1bar and 10 degC at surface
data.incon[grid.blocklist[0].name] = [0, [1.013e5, 10,0, 0, 0]]
#print (grid.blocklist[0].name, '10.0', '1.013e5')
for i in range(1,N):
    name = grid.blocklist[i].name
    elev = grid.block[name].centre[2]
    if elev > -1000:
        temperature = 10 + 0.28 * abs(elev)
    if elev < -1000:
        temperature = 270 + 0.02 * abs(elev)
    p_mpa = p_last/1e6
    t_k = temperature+273.15
    (density, u) = cowat(temperature, p_last)
    pressure = p_last + density * 9.81 * 100
    p_last = pressure
    #print (grid.blocklist[i].name, temperature, pressure)
    data.incon[grid.blocklist[i].name] = [0, [pressure, temperature,0, 0, 0]]

# add source and sink
source = t2generator()
source.name = 'src01'
source.block = block1.name
source.gx = -rate
source.ex = 0
data.add_generator(source)

# Set fixed state
block0.volume = 0   # do not use -ve volumes in pyTough!
grid.demote_block(block0.name)

# write to file
print("Write to file...")
data.write("T2/RunMe.t2")
data.write("Brynhild/RunMe.t2")
print("...done!")


