#!/usr/bin/python3

"""

Create a TOUGH2 model for the MINC1 test case

"""

from t2data import *
from mulgrids import *
from t2grids import *
import numpy as np

# setup the grid
x = np.array([20]*25)
y = np.array([20]*25)
z = np.array([100])
geo = mulgrid().rectangular(x, y, z)
grid = t2grid().fromgeo(geo)

N = 25*25

# first and last block
block0 = grid.blocklist[0]
block1 = grid.blocklist[-1]

# add rock types and material functions
relperm = {'parameters' : [], 'type' : []}
r0 = rocktype(name = 'POMED', permeability = [100e-15,100e-15, 2e-15], specific_heat = 1000, density = 2500, porosity = 0.9)
r0.conductivity = 1
r0.dry_conductivity = r0.conductivity
r0.capillarity = {'parameters' : [0.0] * 7, 'type' : 8}
r0.relative_permeability = {'parameters' : [0.30, 0.1, 0, 0, 0, 0, 0], 'type' : 3}
r0.nad = 2 # set this to activate material functions to be written to file
grid.add_rocktype(r0)

relperm = {'parameters' : [], 'type' : []}
r1 = rocktype(name = 'FRACT', permeability = [100e-15,100e-15, 2e-15], specific_heat = 1000, density = 2500, porosity = 0.9)
r1.conductivity = 1
r1.dry_conductivity = r1.conductivity
r1.capillarity = {'parameters' : [0.0] * 7, 'type' : 8}
r1.relative_permeability = {'parameters' : [0.30, 0.1, 0, 0, 0, 0, 0], 'type' : 3}
r1.nad = 2 # set this to activate material functions to be written to file
grid.add_rocktype(r1)

r2 = rocktype(name = 'MATRX', permeability = [0.01e-15,0.01e-15, 0.01e-15], specific_heat = 1000, density = 2500, porosity = 0.15)
r2.conductivity = 1
r2.dry_conductivity = r2.conductivity
r2.capillarity = {'parameters' : [0.0] * 7, 'type' : 8}
r2.relative_permeability = {'parameters' : [0.30, 0.1, 0, 0, 0, 0, 0], 'type' : 3}
r2.nad = 2 # set this to activate material functions to be written to file
grid.add_rocktype(r2)


# set the rock type for the blocks
for i in range(N):
    grid.blocklist[i].rocktype = r0
        
#grid.minc(volume_fractions = [0.1, 0.9], spacing=50., num_fracture_planes=3, blocks=None, matrix_blockname=None, minc_rockname=None, proximity=None, atmos_volume=1.e25, incon='y', fracture_connection_distance=0.)


 
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
data.parameter['max_timestep'] = 60*60*24*365*0.5
data.parameter['timestep_reduction'] = 4.0
data.parameter['print_interval'] = 9999
data.parameter['max_iterations'] = 8
data.parameter['absolute_error'] = 1.0
data.parameter['relative_error'] = 1.0e-5
data.parameter['upstream_weight'] = 1.0
data.parameter['newton_weight'] = 1.0
data.parameter['derivative_increment'] = 0.14901e-7
data.parameter['scale'] = 1.0
data.parameter['option'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 3, 0, 3, 0, 0, 3, 0, 0, 0]  # note: this has a MOP[0], but syntax should use mop 1 as MOP[1]
data.parameter['default_incons'] = [100e5, 304]

# set the print times
data.output_times['time'] =  (np.arange(0,11,1.0) * 365 * 24 * 60 * 60).tolist()
data.output_times['num_times_specified'] = len(data.output_times['time'])

data.start = True

# set the initial conditions
for i in range(N):
    name = grid.blocklist[i].name
    #data.incon[grid.blocklist[i].name] = [0, [100e5,304,0, 0, 0]]
    x = grid.block[name].centre[0]
    y = grid.block[name].centre[1]
    if (x==170) and (y==250):
        prodname = name
    if (x==310) and (y==250):
        injname = name

#
# add source and sink
prod = t2generator()
prod.name = 'prd01'
prod.block = prodname
prod.gx = -12.6
prod.ex = 0
data.add_generator(prod)

inj = t2generator()
inj.name = 'inj01'
inj.block = injname
inj.gx = 12.6
inj.ex = 196e3
data.add_generator(inj)

print("Injector block name:", injname)
print("Producer block name:", prodname)


# the fracture spacings
# note: use integers here since the subfolders are named by the fracture spacings
FracSpacs = [300, 50]

for FS in FracSpacs:
    path = "FS%d" % FS
    data.meshmaker = [('minc', {'dual': '' , 'num_continua': 3, 'spacing': [FS], 'type': 'THRED', 'vol': [0.1, 0.2], 'where': 'OUT'})]
    # write to file
    print("Write to file...")
    data.write(path + "/T2/RunMe.t2")
    data.write(path + "/Brynhild/RunMe.t2")
    grid.write_vtk(geo, path + "/Brynhild/MINC1.vtu")

print("...done!")


