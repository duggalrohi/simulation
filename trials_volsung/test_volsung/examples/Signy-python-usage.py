#!/usr/bin/python3

"""
Example script for demonstrating the use of the Signy thermodynamic table tool by calling
it from python.

For more information directly inspect the signy.py source code.
"""

from volsung.signy import *

#
# Create two thermodynamic tables to compare their thermophysical properties
# See signy.py for the available classes
#

table_iapws = TT_IAPWSIF97()              # table for pure H2O
table_CO2   = TT_CO2()                    # table for H2O + CO2

#
# Set the table
#
# There are different setter methods, i.e.
#
# phX - pressure, enthalpy, bulk mass fractions
# pTX - pressure, temperature, bulk mass fractions
# pxX - pressure, gas mass fraction (quality), bulk mass fractions
# TxX - temperature, gas mass fraction (quality), bulk mass fractions
#
# however not all thermodynamic tables support all different setter methods.
#
# Note: all units used are strictly SI, in particular use pressure in Pa, temperature in K, enthalpy in J/kg

iapws_valid = table_iapws.set_phX(1e5, 84e3)
co2_valid   = table_CO2.set_phX(1e5, 84e3, X = {'XCO2' : 0.01})

# it is always a good idea to check that the tables are valid, i.e. they support the setter method
# and the primary variables used as arguments lead to a valid thermodynamic state
# the output() method can sometimes provide more information

if not iapws_valid:
    print(table_iapws.output())
if not co2_valid:
    print(table_CO2.output())
    
#
# access some bulk thermodynamical properties
#
print("Some bulk properties...")
print()
print("T(H2O,bulk)       [degC]  = {}".format(table_iapws.Temperature - 273.15))
print("T(H2O + CO2,bulk) [degC]  = {}".format(table_CO2.Temperature - 273.15))
print("h(H2O,bulk)       [kJ/kg] = {}".format(table_iapws.Enthalpy * 1e-3))
print("h(H2O + CO2,bulk) [kJ/kg] = {}".format(table_CO2.Enthalpy * 1e-3))
print()
#
# for more information about bulk properties use the dir() command
#
print(dir(table_iapws))
print()
print()

#
# access some phase specific thermodynamical properties
#
print("Some phase properties...")
print()
print("Saturation (H2O, liquid)                = {}".format(table_iapws.Phase['liquid'].Saturation))
print("Saturation (H2O + CO2, liquid)          = {}".format(table_CO2.Phase['liquid'].Saturation))
print("MassFraction of H2O (H2O, liquid)       = {}".format(table_iapws.Phase['liquid'].MassFraction['H2O']))
print("MassFraction of H2O (H2O + CO2, liquid) = {}".format(table_CO2.Phase['liquid'].MassFraction['H2O']))
print("MassFraction of CO2 (H2O + CO2, liquid) = {}".format(table_CO2.Phase['liquid'].MassFraction['CO2']))
print()
#
# for more information about phase properties use the dir() command on a phase
#
print(dir(table_iapws.Phase['gas']))
print()
print()
