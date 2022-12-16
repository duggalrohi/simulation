% Define the working fluid and the pressure and temperature ranges
fluid = 'R245fa';
p_low = 1e5; % Low pressure (Pa)
p_high = 3e5; % High pressure (Pa)
T_low = 300; % Low temperature (K)
T_high = 500; % High temperature (K)

% Define the turbine efficiency
eta_t = 0.8; % Turbine efficiency

% Define the mass flow rate of the working fluid
m_dot = 1; % Mass flow rate (kg/s)

% Calculate the enthalpy at the low and high pressure and temperature points
h_low = CoolProp.PropsSI('H', 'T', T_low, 'P', p_low, fluid);
h_high = CoolProp.PropsSI('H', 'T', T_high, 'P', p_high, fluid);

% Calculate the work output of the turbine
W_turbine = m_dot * (h_high - h_low) * eta_t;

% Calculate the enthalpy at the turbine outlet
h_turbine_outlet = h_low + W_turbine / m_dot;

% Calculate the pressure at the turbine outlet
p_turbine_outlet = CoolProp.PropsSI('P', 'H', h_turbine_outlet, 'T', T_low, fluid);

% Calculate the isentropic efficiency of the pump
s_low = CoolProp.PropsSI('S', 'T', T_low, 'P', p_low, fluid);
s_turbine_outlet = CoolProp.PropsSI('S', 'H', h_turbine_outlet, 'P', p_turbine_outlet, fluid);
eta_p = (s_turbine_outlet - s_low) / (s_high - s_low);

% Calculate the work input to the pump
W_pump = m_dot * (h_high - h_turbine_outlet) / eta_p;

% Calculate the net work output of the cycle
W_net = W_turbine - W_pump;

% Calculate the thermal efficiency of the cycle
Q_in = m_dot * (h_high - h_low);
eta_th = W_net / Q_in;

% Print the results
fprintf('Turbine work output: %f J/s\n', W_turbine);
fprintf('Pump work input: %f J/s\n', W_pump);
fprintf('Net work output: %f J/s\n', W_net);
fprintf('Thermal efficiency: %f\n', eta_th);
