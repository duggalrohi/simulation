import clr

from System.IO import Directory, Path, File
from System import String, Double, Array, Reflection, Exception


import os
from os.path import expanduser
#dtlpath = "C:\\Users\\Daniel\\Source\\Repos\\DanWBR\\dwsim6\\DistPackages\\DTL\\"
dtlpath = os.path.expanduser('~\\Source\\Repos\\dwsim\\DistPackages\\DTL\\')


clr.AddReference(dtlpath + "DWSIM.Thermodynamics.StandaloneLibrary.dll")

from DWSIM.Thermodynamics import Streams, PropertyPackages, CalculatorInterface

import CapeOpen

dtlc = CalculatorInterface.Calculator()

print(String.Format("DTL version: {0}", Reflection.Assembly.GetAssembly(dtlc.GetType()).GetName().Version))
print()

dtlc.Initialize()

nrtl = PropertyPackages.NRTLPropertyPackage(True)

dtlc.TransferCompounds(nrtl)

T = 355.0 #K
P = 101325.0 #Pa

compprops = dtlc.GetCompoundConstPropList()

print("Ethanol constant properties:\n")
for prop in compprops:
    pval = dtlc.GetCompoundConstProp("Ethanol", prop)
    print(prop + "\t" + pval)

print()

compprops = dtlc.GetCompoundPDepPropList()

print()
print("Ethanol pressure-dependent properties at P = " + str(P) + " Pa:\n")
for prop in compprops:
    pval = dtlc.GetCompoundPDepProp("Ethanol", prop, P)
    print(prop + "\t" + pval)

print()

compprops = dtlc.GetCompoundTDepPropList()

print()
print("Ethanol temperature-dependent properties at T = " + str(T) + " K:\n")
for prop in compprops:
    pval = dtlc.GetCompoundTDepProp("Ethanol", prop, T)
    print(prop + "\t" + pval)

print()

print()
print("Water/Ethanol Interaction Parameters for NRTL model:")
print()

# uncheck this if you have a CUDA or OpenCL device to use
# dtlc.EnableGPUProcessing()
# dtlc.InitComputeDevice(Cudafy.eLanguage.Cuda, 0)

ip = dtlc.GetInteractionParameterSet("NRTL", "Water", "Ethanol")
print("A12 = " + str(ip.Parameters["A12"]) + " cal/mol")
print("A21 = " + str(ip.Parameters["A21"]) + " cal/mol")
print("alpha = " + str(ip.Parameters["alpha"]))

print("PT Flash of an equimolar mixture of Water and Ethanol at T = " + str(T) + " K and P = " + str(P) + " Pa:" + "\n")
print("Using NRTL model for equilibrim calculations.")
print()

carray = Array[String](["Water", "Ethanol"])
comparray = Array[Double]([0.5, 0.5])

result2 = dtlc.PTFlash(nrtl, 0, P, T, carray, comparray)

print()
print("Flash calculation results:")
print()

for i in range(0, result2.GetLength(0)):
    if (i == 0):
        line = "Phase Name" + "\t"
    elif (i == 1):
        line = "Phase Mole Fraction in Mixture" + "\t"
    elif (i == 2):
        line = "Water Mole Fraction in Phase" + "\t"
    elif (i == 3):
        line = "Ethanol Mole Fraction in Phase" + "\t"
    else:
        line = ""
    for j in range(0, result2.GetLength(1)):
        line += str(result2[i, j])
    print(line)

print()
print("Vapor Phase Mixture Properties at T = " + str(T) + " K and P = " + str(P) + " Pa:" + "\n")

vcarray = Array[Double]([float(result2[2, 0]), float(result2[3, 0])])

compphaseprops = dtlc.GetPropList()
for prop in compphaseprops:
    try:
        values = dtlc.CalcProp(nrtl, prop, "Mole", "Vapor", carray, T, P, vcarray)
        line = ""
        for i in range(0, values.Length):
            line += str(values[i]) + "\t"
        print(prop + "\t" + line)
    except CapeOpen.CapeThrmPropertyNotAvailableException as e:
        print(prop + "\t" + "Property Not Available")
    except CapeOpen.CapeComputationException as e:
        print(prop + "\t" + "Error Calculating Property")
    except Exception as e:
        print(prop + "\t" + e.Message)

print()
print("Liquid Phase Mixture Properties at T = " + str(T) + " K and P = " + str(P) + " Pa:" + "\n")

lcarray = Array[Double]([float(result2[2, 1]), float(result2[3, 1])])

for prop in compphaseprops:
    try:
        values = dtlc.CalcProp(nrtl, prop, "Mole", "Liquid", carray, T, P, lcarray)
        line = ""
        for i in range(0, values.Length):
            line += str(values[i]) + "\t"
        print(prop + "\t" + line)
    except CapeOpen.CapeThrmPropertyNotAvailableException as e:
        print(prop + "\t" + "Property Not Available")
    except CapeOpen.CapeComputationException as e:
        print(prop + "\t" + "Error Calculating Property")
    except Exception as e:
        print(prop + "\t" + e.Message)