#!/usr/bin/python3

"""

Create a TOUGH2 model of Stanford Test Problem #6

"""

from t2data import *
from mulgrids import *
from t2grids import *
from IAPWS97 import *
import numpy as np


# setup the grid
yspace = 4000/5
x = np.array([1000]*5)
y = np.array([yspace]*5)
z = np.array([2,300,300,300, 300,600,2])
geo = mulgrid().rectangular(x, y, z)
grid = t2grid().fromgeo(geo)

N = 25*7

# first and last block
block0 = grid.blocklist[0]
block1 = grid.blocklist[-1]

# add rock types and material functions
relperm = {'parameters' : [], 'type' : []}
r0 = rocktype(name = 'rock0', permeability = [100e-15,100e-15, 2e-15], specific_heat = 1000, density = 2500, porosity = 0.2)
r0.conductivity = 1
r0.dry_conductivity = r0.conductivity
r0.capillarity = {'parameters' : [0.0] * 7, 'type' : 8}
r0.relative_permeability = {'parameters' : [0.30, 0.1, 0, 0, 0, 0, 0], 'type' : 3}
r0.nad = 2 # set this to activate material functions to be written to file
grid.add_rocktype(r0)

r1 = rocktype(name = 'rock1', permeability = [200e-15,200e-15, 50e-15], specific_heat = 1000, density = 2500, porosity = 0.25)
r1.conductivity = 1
r1.dry_conductivity = r1.conductivity
r1.capillarity = {'parameters' : [0.0] * 7, 'type' : 8}
r1.relative_permeability = {'parameters' : [0.30, 0.1, 0, 0, 0, 0, 0], 'type' : 3}
r1.nad = 2 # set this to activate material functions to be written to file
grid.add_rocktype(r1)



# set the rock type for the blocks
for i in range(N):
    name = grid.blocklist[i].name
    z = grid.block[name].centre[2]
    if (z==-1) or (z == -152) or (z == -1502) or (z == -1802):
        grid.blocklist[i].rocktype = r0
    else:
        grid.blocklist[i].rocktype = r1
        
    
# create the TOUGH2 input file
data = t2data()
data.grid = grid

# create global material functions for rocks which don't posess any
data.capillarity = r0.capillarity
data.relative_permeability = r0.relative_permeability

# set the parameter section
data.parameter['gravity'] = 9.81
data.parameter['max_timesteps'] = 9999
data.parameter['tstart'] = 0
data.parameter['tstop'] = data.parameter['tstart'] + 60*60*24*365*10
data.parameter['const_timestep'] = 60*60*24*365*0.1
data.parameter['max_timestep'] = 60*60*24*365*0.1
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



l4_t = 280
l4_p = sat(280)
l4_rho, u = cowat(l4_t, l4_p)

l5_t = 160
l5_rho, u = cowat(l5_t, sat(l5_t))
l5_p = l4_p - 1470 * (l4_rho + l5_rho)

l3_t = 280
l3_rho, u = cowat(l3_t, sat(l3_t))
l3_p = l4_p + 1470 * (l3_rho + l4_rho)

l2_t = 280
l2_rho, u = cowat(l2_t, sat(l2_t))
l2_p = l3_p + 1470 * (l2_rho + l3_rho)

l1_t = 280
l1_rho, u =  cowat(l1_t, sat(l1_t))
l1_p = l2_p + 1470 * (l1_rho + l2_rho)

ltop_p = l5_p - 1*9.81 * l5_rho
ltop_t = 100

lbase_p = l1_p + 1*9.81 * l1_rho
lbase_t = 280


#print(ltop_p/1e5, ltop_t);
#print(l5_p/1e5, l5_t);
#print(l4_p/1e5, l4_t);
#print(l3_p/1e5, l3_t);
#print(l2_p/1e5, l2_t);
#print(l1_p/1e5, l1_t);
#print(lbase_p/1e5, lbase_t);
# set the initial conditions
for i in range(N):
    name = grid.blocklist[i].name
    z = grid.block[name].centre[2]
    if (z == -1):
        data.incon[grid.blocklist[i].name] = [0, [ltop_p,ltop_t,0, 0, 0]]
    if (z == -152):
        data.incon[grid.blocklist[i].name] = [0, [l5_p,l5_t,0, 0, 0]]
    elif (z == -452):
        data.incon[grid.blocklist[i].name] = [0, [l4_p,0.1,0, 0, 0]]
    elif (z == -752):
        data.incon[grid.blocklist[i].name] = [0, [l3_p,l3_t,0, 0, 0]]
    elif (z == -1052):
        data.incon[grid.blocklist[i].name] = [0, [l2_p,l2_t,0, 0, 0]]
        x = grid.block[name].centre[0]
        y = grid.block[name].centre[1]
        if (x<1000) and (y<yspace):
            sourcename = name
            print (name)
    elif (z == -1502):
        data.incon[grid.blocklist[i].name] = [0, [l1_p,l1_t,0, 0, 0]]
    elif (z == -1803):
        data.incon[grid.blocklist[i].name] = [0, [lbase_p,lbase_t,0, 0, 0]]
        


# add source and sink
source = t2generator()
source.name = 'src01'
source.block = sourcename
source.ltab = 4
source.time = np.array([0,2,4,6])*60*60*24*365
source.rate = np.array([-1000,-2500,-4000, -6000])
data.add_generator(source)


# Set fixed state
fixedblocks = []
for i in range(N):
    name = grid.blocklist[i].name
    x = grid.block[name].centre[0]
    z = grid.block[name].centre[2]
    if (z == -1) or (z == -1803) or (x>4000):
        block = grid.blocklist[i]
        block.volume = 0   # do not use -ve volumes in pyTough!
        fixedblocks.append(block.name)
for fixedblock in fixedblocks:
    grid.demote_block(fixedblock)

# write to file
print("Write to file...")
data.write("T2/RunMe.t2")
data.write("Brynhild/RunMe.t2")
grid.write_vtk(geo, "Brynhild/Stanford6.vtu")
print("...done!")


