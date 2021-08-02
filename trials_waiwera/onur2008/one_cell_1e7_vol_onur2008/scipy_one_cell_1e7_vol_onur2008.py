'''Solve lumped parameter model using scipy ode module
'''

import scipy.integrate
import matplotlib.pyplot as pyplot
import numpy
import iapws


def DensityWater(P,T):
    '''Density of water at temperature T (deg C) and Pressure, P (Pa)
    '''
    state = iapws.IAPWS97(P=P/1.0e6, T=T+273.15)
    rho = state.rho
    # rho = -6.621e-8*T*T*T*T + 3.95337e-5*T*T*T - 1.00637e-2*T*T + 3.018277e-1*T + 996.112
    return rho
    
    
def RHSFun(t, P, P0, W, Sm, alpha):
    '''RHS of eqn
    '''
    Wr = alpha*(P0 - P)
    return (Wr - W)/Sm    # (m, e)


def Solve(P0, W, V, phi, c, alpha, t0, t1, nt):
    '''Solve the lumped paramter equation
       dP/dt = (Wr - W)/Sm
    '''
    solver = scipy.integrate.ode(RHSFun).set_integrator('vode', method='bdf')
    solver.set_initial_value(P0, t0)

    soln = []
    
    T = 140.0
    T = 25.0
    
    dt = (t1 - t0)/nt
    P = P0
    dP = 1.0e3
    while solver.successful() and solver.t < t1:
        rho = DensityWater(P, T)
        P1 = P + dP
        rho1 = DensityWater(P1, T) 
        c = (rho1 - rho)/dP / rho
        Sm = V*phi*rho*c
        solver.set_f_params(P0, W, Sm, alpha)
        P = solver.integrate(solver.t + dt)[0]
        soln.append((solver.t, P))
        print('P, Rho, c, Sm', P, rho, c, Sm)
        
    # print(soln)
    soln = numpy.array(soln)
    pyplot.clf()
    pyplot.plot(soln[:, 0], soln[:, 1])
    pyplot.show()
    
    
P0 = 50.0e5
c = 1.33e-9
V = 1e7
phi = 0.2
alpha = 0
t0 = 0
t1 = 10*24*3600
nt = 20

W = 5.0

print('Solving model with W =', W)
Solve(P0, W, V, phi, c, alpha, t0, t1, nt)
