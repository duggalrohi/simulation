#!/usr/bin/python3

"""

This script demonstrates the basic, safe usage of Volsung in combination with PEST/BEOPEST

"""

import os
import sys
import subprocess

from volsung.volsungmodel import *

ModelFile = "columnPEST.brynhild"                   # this is the same name as given in the control file for the modified model template
ObsFile = "Observations.txt"                        # this is the file we will write the observations we extracted from Results.sigurd to
Remote = ""

# Only set par2parFile if you are working with constrained parameters.
# In this case prepare an intermediate template file as described in section 7 of the second PEST manual
# and use reference to the par2parFile inside the control file instead of referencing the 
# model template file directly
par2parFile  = ""                                   # the par2par template file; leave blank if not working with constrained parameters      

#
# 1. Ensure that any previous output file containing the observations gets deleted
#    This prevents PEST finding an old file in case the model run failed
#
try:
    os.remove(ObsFile)
except:
    pass
try:
    os.remove("Results.sigurd")
except:
    pass

#
# 2. Run the PAR2PAR command if required
#
if par2parFile != "":
    cmd = "par2par " + par2parFile
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    while p.poll() is None:
        l = p.stdout.readline() # This blocks until it receives a newline.
        msg = l.decode("utf-8").strip("\n")
        print(msg)
        if msg.find('Cannot open PAR2PAR input file') >= 0:
            exit(-1)
    msg = l.decode("utf-8").strip("\n")            
    print(msg)
    if msg.find('Cannot open PAR2PAR input file') >= 0:
        exit(-1)

#
# 3. Create the run command and arguments
#    
brynhildcmd = "brynhild"
if sys.platform == "win32":
    brynhildcmd = '"C:/Program Files/Volsung/Brynhild"'
    
args = [brynhildcmd, ModelFile, "--run", "--verbose", "--hide"]
if Remote != "":
    args += [" --remote", Remote]
    
#
# 4. Execute the cmd and wait for it to finish
#  
cmd = " ".join(args)
print("Executing the following run command:")
print(cmd)
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
while p.poll() is None:
    l = p.stdout.readline() # This blocks until it receives a newline.
    print(l.decode("utf-8").strip("\n"))
print(p.stdout.read().decode("utf-8"))
# was there an error running the simulation?
if p.returncode != 0:
    print("The run process finished with an error, exit code = ", p.returncode)
    exit(p.returncode)


#
# 5. Read in the model results and output the desired observations
#    This part depends on the actual model and should be edited accordingly
#
print("Reading in model output...")
model = VolsungModel("Results.sigurd")
output = open(ObsFile, "w")
# check that the end time was reached
if not model.reservoir.endTimeReached():
    print("Simulation did not reach end time; abort.")
    exit(-1)
# establish the pressure history and grab the pressure from the last print time
p = model.reservoir.history("/reservoir/Elements/Pressure")[-1]
cellIds = model.reservoir.history("/reservoir/Elements/Cell Id")[-1]
for i in range(p.size):
    cid = cellIds[i]
    if (cid >= 0):
        output.write("p%d=%f\n" % (cellIds[i], p[i]))
output.close()
