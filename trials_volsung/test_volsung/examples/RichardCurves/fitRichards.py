#!/usr/bin/python3

"""

fitRichards.py

A simple script to fit a Richard's curve to a data set with the intention to
use the Richard's curve for describing a relative permeability function.

See https://en.wikipedia.org/wiki/Generalised_logistic_function

"""

import numpy
import math
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

#
# the data to fit the curve to
# you will need to provide liquid saturations S_liq and relative permeabilities kr for both the liquid and gas phase
# 
# remember that kr(0) = 0 and kr(1) = 1 are mandatory
#
# note: if you want to put more emphasis on a particular part of the curve then insert denser data there
#

S_liq  = numpy.array([0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.52, 0.54, 0.56, 0.58, 0.60, 0.70, 0.80, 0.90, 1.00])
kr_liq = numpy.array([0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.25, 0.50, 0.75, 1.00])

S_gas =  numpy.array([1.00, 0.30, 0.20, 0.10, 1.00])
kr_gas = numpy.array([1.00, 0.75, 0.50, 0.25, 0.00])

#
# initial guess for the function parameters
#

B0_liq = 20
C0_liq = 0.5
Q0_liq = 1e8
v0_liq = 1.5

B0_gas = 100
C0_gas = 1.0
Q0_gas = 1e8
v0_gas = 2

#
# define the Richard's curve
#
def richards(S, B, C, Q, v):
    # calculate the auxiliary parameters u,w
    u = (C+Q)**(1/v)
    w = (C+Q * math.exp(-B))**(1/v)
    # calculate the constrained parameters A, K
    A = w/(w - u)
    K = -A * (u - 1)
    # calculate the function and return its value
    k = A + (K-A) / (C + Q * numpy.exp(-B * S))**(1/v)
    return k

#
# define the fit parameter array and its boundaries
#
p0_liq = numpy.array([B0_liq, C0_liq, Q0_liq, v0_liq])
p0_gas = numpy.array([B0_gas, C0_gas, Q0_gas, v0_gas])
bounds_liq = ([0, 0, 0, 0.01],
              [10000, 10000, 1e10, 100])
bounds_gas = bounds_liq

#
# perform the curve fit
# 
popt_liq, pcov_liq = curve_fit(richards, S_liq, kr_liq, p0 = p0_liq, bounds = bounds_liq)
popt_gas, pcov_gas = curve_fit(richards, S_gas, kr_gas, p0 = p0_gas, bounds = bounds_gas)

#
# print the results and show a plot for comparison
#
B_liq = popt_liq[0]
C_liq = popt_liq[1]
Q_liq = popt_liq[2]
v_liq = popt_liq[3]

print('Parameters for liquid relative permeability curve:')
print('B = %f' % B_liq)
print('C = %f' % C_liq)
print('Q = %f' % Q_liq)
print('v = %f' % v_liq)
print()

B_gas = popt_gas[0]
C_gas = popt_gas[1]
Q_gas = popt_gas[2]
v_gas = popt_gas[3]

print('Parameters for gas relative permeability curve:')
print('B = %f' % B_gas)
print('C = %f' % C_gas)
print('Q = %f' % Q_gas)
print('v = %f' % v_gas)
print()

Sl = numpy.linspace(0, 1, 50)
Sg = 1.0 - Sl

plt.figure()
plt.plot(S_liq, kr_liq, 'o')
plt.plot(Sl, richards(Sl, B_liq, C_liq, Q_liq, v_liq), '-', label = '$kr_{liq}$')
plt.plot(1.0 - S_gas, kr_gas, 'x')
plt.plot(Sg, richards(Sl, B_gas, C_gas, Q_gas, v_gas), '-', label = '$kr_{gas}$')
plt.xlabel("Saturation (liquid)")
plt.ylabel("kr")
plt.legend()
plt.title("Richard S-Curve - Fitted Functions")