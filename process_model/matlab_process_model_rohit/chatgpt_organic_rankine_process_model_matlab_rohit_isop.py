import CoolProp.CoolProp as CP

# Constants
fluid = 'Isopentane' # Working fluid
T_ambient = 298.15 # Ambient temperature [K]
P_ambient = 101325 # Ambient pressure [Pa]

# Cycle parameters
T_boiler_in = 473.15 # Boiler inlet temperature [K]
T_boiler_out = 363.15 # Boiler outlet temperature [K]
T_condenser_in = 363.15 # Condenser inlet temperature [K]
T_condenser_out = 298.15 # Condenser outlet temperature [K]
P_boiler_out = 8.5e5 # Boiler outlet pressure [Pa]
P_condenser_out = 101325 # Condenser outlet pressure [Pa]

# Calculate enthalpy at each state
h_1 = CP.PropsSI('H', 'T', T_boiler_in, 'P', P_ambient, fluid) # Enthalpy at state 1 [J/kg]
h_2 = CP.PropsSI('H', 'T', T_boiler_out, 'P', P_boiler_out, fluid) # Enthalpy at state 2 [J/kg]
h_3 = CP.PropsSI('H', 'T', T_condenser_in, 'P', P_boiler_out, fluid) # Enthalpy at state 3 [J/kg]
h_4 = CP.PropsSI('H', 'T', T_condenser_out, 'P', P_condenser_out, fluid) # Enthalpy at state 4 [J/kg]

# Calculate enthalpy change for each process
dh_12 = h_2 - h_1 # Enthalpy change for process 1-2 [J/kg]
dh_23 = h_3 - h_2 # Enthalpy change for process 2-3 [J/kg]
dh_34 = h_4 - h_3 # Enthalpy change for process 3-4 [J/kg]
dh_41 = h_1 - h_4 # Enthalpy change for process 4-1 [J/kg]

# Calculate work and heat transfer for each process
W_12 = P_boiler_out*(V_2 - V_1) # Work for process 1-2 [J/kg]
Q_in = dh_12 - W_12 # Heat transfer for process 1-2 [J/kg]
W_23 = P_condenser_out*(V_3 - V_2) # Work for process 2-3 [J/kg]
Q_out = dh_34 + W_23 # Heat transfer for process 3-4 [J/kg]

# Calculate cycle efficiency
eta = (W_12 + W_23)/Q_in # Cycle efficiency [-]

# Calculate size of heat exchanger
# Assume heat exchanger effectiveness is 0.8
# Calculate heat transfer rate from inlet to outlet fluid
Q = Q_in/(1 - 0.8) # Heat transfer rate [W]

# Calculate heat exchanger area
A = Q/(0.8*





import numpy as np

# Constants
M_isopentane = 72.15 # Molecular weight of isopentane [g/mol]
R_const = 8.31446 # Universal gas constant [J/mol*K]
T_ambient = 298.15 # Ambient temperature [K]
P_ambient = 101325 # Ambient pressure [Pa]

# Cycle parameters
T_boiler_in = 473.15 # Boiler inlet temperature [K]
T_boiler_out = 363.15 # Boiler outlet temperature [K]
T_condenser_in = 363.15 # Condenser inlet temperature [K]
T_condenser_out = 298.15 # Condenser outlet temperature [K]
P_boiler_out = 8.5e5 # Boiler outlet pressure [Pa]
P_condenser_out = 101325 # Condenser outlet pressure [Pa]

# Calculate enthalpy at each state
h_1 = (2501.2 + (R_const/M_isopentane)*T_boiler_in)*1000 # Enthalpy at state 1 [J/kg]
h_2 = (2501.2 + (R_const/M_isopentane)*T_boiler_out)*1000 # Enthalpy at state 2 [J/kg]
h_3 = (2501.2 + (R_const/M_isopentane)*T_condenser_in)*1000 # Enthalpy at state 3 [J/kg]
h_4 = (2501.2 + (R_const/M_isopentane)*T_condenser_out)*1000 # Enthalpy at state 4 [J/kg]

# Calculate enthalpy change for each process
dh_12 = h_2 - h_1 # Enthalpy change for process 1-2 [J/kg]
dh_23 = h_3 - h_2 # Enthalpy change for process 2-3 [J/kg]
dh_34 = h_4 - h_3 # Enthalpy change for process 3-4 [J/kg]
dh_41 = h_1 - h_4 # Enthalpy change for process 4-1 [J/kg]

# Calculate work and heat transfer for each process
W_12 = P_boiler_out*(V_2 - V_1) # Work for process 1-2 [J/kg]
Q_in = dh_12 - W_12 # Heat transfer for process 1-2 [J/kg]
W_23 = P_condenser_out*(V_3 - V_2) # Work for process 2-3 [J/kg]
Q_out = dh_34 + W_23 # Heat transfer for process 3-4 [J/kg]

# Calculate cycle efficiency
eta = (W_12 + W_23)/Q_in # Cycle efficiency [-]

# Calculate size of heat exchanger
# Assume heat exchanger effectiveness is 0.8
# Calculate heat transfer rate from inlet to outlet fluid
Q = Q_in/(1 - 0.8) # Heat transfer rate [W]

# Calculate heat exchanger area
A = Q/(


# Import necessary libraries
import math
import CoolProp.CoolProp as CP

# Define input data
m = 0.5 # Mass flow rate of hot fluid, in kg/s
T1 = 300 # Inlet temperature of hot fluid, in K
T2 = 280 # Outlet temperature of cold fluid, in K
U = 500 # Overall heat transfer coefficient, in W/m^2K
fluid = 'water' # Name of hot fluid

# Calculate specific heat capacity of hot fluid using CoolProp
Cp = CP.PropsSI('C', 'T', T1, 'P', 101325, fluid)

# Calculate heat transfer rate using mass flow rate and specific heat capacity
Q = m * Cp * (T1 - T2)

# Calculate heat exchanger area
A = Q / (U * (T1 - T2))
print("Heat exchanger area: {} m^2".format(A))

import CoolProp.CoolProp as CP

# Define input data
T1 = 500 # Inlet temperature of hot fluid, in K
T2 = 300 # Outlet temperature of cold fluid, in K
P1 = 10 * 1e5 # Inlet pressure of isopentane, in Pa
P2 = 5 * 1e5 # Outlet pressure of isopentane, in Pa
fluid = 'Isopentane' # Name of working fluid

# Calculate specific heat capacity of isopentane using CoolProp
Cp = CP.PropsSI('C', 'T', T1, 'P', P1, fluid)

# Calculate mass flow rate of isopentane using energy balance
Q_in = 20000 # Heat input to ORC, in W
W_out = 10000 # Work output from ORC, in W
m = Q_in / (Cp * (T1 - T2)) # Mass flow rate of isopentane, in kg/s

# Calculate enthalpy of isopentane at inlet and outlet using CoolProp
h1 = CP.PropsSI('H', 'T', T1, 'P', P1, fluid) # Enthalpy at inlet, in J/kg
h2 = CP.PropsSI('H', 'T', T2, 'P', P2, fluid) # Enthalpy at outlet, in J/kg

# Calculate thermal efficiency of ORC
eta = W_out / Q_in

# Print results
print("Mass flow rate of isopentane: {} kg/s".format(m))
print("Thermal efficiency of ORC: {:.2f}".format(eta))







import CoolProp.CoolProp as CP

# Define input data
T1 = 500 # Inlet temperature of hot fluid, in K
T2 = 300 # Outlet temperature of cold fluid, in K
T3 = 280 # Inlet temperature of isopentane, in K
P1 = 10 * 1e5 # Inlet pressure of isopentane, in Pa
P2 = 5 * 1e5 # Outlet pressure of isopentane, in Pa
fluid = 'Isopentane' # Name of working fluid

# Calculate specific heat capacity of isopentane using CoolProp
Cp = CP.PropsSI('C', 'T', T1, 'P', P1, fluid)

# Calculate mass flow rate of isopentane using energy balance
Q_in = 20000 # Heat input to ORC, in W
W_out = 10000 # Work output from ORC, in W
Q_preheater = 1000 # Heat transfer rate in preheater, in W
m = (Q_in - Q_preheater) / (Cp * (T1 - T3)) # Mass flow rate of isopentane, in kg/s

# Calculate enthalpy of isopentane at inlet and outlet using CoolProp
h1 = CP.PropsSI('H', 'T', T3, 'P', P1, fluid) # Enthalpy at inlet, in J/kg
h2 = CP.PropsSI('H', 'T', T2, 'P', P2, fluid) # Enthalpy at outlet, in J/kg

# Calculate thermal efficiency of ORC
eta = W_out / (Q_in - Q_preheater)

# Print results
print("Mass flow rate of isopentane: {} kg/s".format(m))
print("Thermal efficiency of ORC: {:.2f}".format(eta))



