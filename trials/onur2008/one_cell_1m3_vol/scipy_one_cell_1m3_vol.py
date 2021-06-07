'''Solve lumped parameter model using scipy ode module
'''

import scipy.integrate
import matplotlib.pyplot as pyplot
import numpy


def DensityWater(T):
    '''Approximation of density of water with temperature
    '''
    rho = -6.621e-8*T*T*T*T + 3.95337e-5*T*T*T - 1.00637e-2*T*T + 3.018277e-1*T + 996.112
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
    
    T = 18.5
    
    dt = (t1 - t0)/nt
    while solver.successful() and solver.t < t1:
        rho = DensityWater(T)
        Sm = V*phi*rho*c
        print('Sm', rho, Sm)
        solver.set_f_params(P0, W, Sm, alpha)
        val = solver.integrate(solver.t + dt)
        soln.append((solver.t, val))
        
    # print(soln)
    soln = numpy.array(soln)
    pyplot.clf()
    pyplot.plot(soln[:, 0], soln[:, 1])
    pyplot.show()
    
    
P0 = 10.0e5
c = 5e-10
V = 1
phi = 0.2
alpha = 0
t0 = 0
t1 = 19
nt = 20

W = 0.0041667

print('Solving model with W =', W)
Solve(P0, W, V, phi, c, alpha, t0, t1, nt)
