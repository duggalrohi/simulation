'''Solve lumped parameter model using scipy ode module
'''

import scipy.integrate 
import matplotlib.pyplot as pyplot
import numpy 
from scipy.integrate._ivp.ivp import METHODS

def DensityWater(T):
    rho = -6.621e-8*T*T*T*T + 3.95337e-5*T*T*T - 1.00637e-2*T*T + 3.018277e-1*T + 996.112
    return rho




def RHSFunT(t, T, B):
    '''RHS of T eqn
    '''
    W_inj = 15
    h_inj = 255300 
    W_p = 20
    h_p = 592216

    R = W_inj*h_inj
    k = W_p*h_p
    return (R - k)/B

def Solve(T0, t0, t1, nt):
    solver = scipy.integrate.ode(RHSFunT).set_integrator('vode', method = 'bdf')
    solver.set_initial_value(T0, t0)

    soln = []

    T = 140

    dt = (t1-t0)/nt
    while solver.successful() and solver.t < t1:
        rho = DensityWater(T)
        B = (((1-phi)*rho_r*C_r*V)+(V*phi*rho*C_w))
        print('<rho_C> is', B)
        solver.set_f_params(T, B)
        val = solver.integrate(solver.t+dt)
        soln.append((solver.t, val))

    soln = numpy.array(soln)
    print('soln is', soln)
    pyplot.clf()
    pyplot.plot(soln[:, 0], soln[:, 1])
    pyplot.show()

t0 = 0
t1 = 10*24*3600
nt = 20
T0 = 140

phi = 0.2
rho_r = 2650
C_r = 1000
C_w = 4200
V = 1e7
 
Solve(T0, t0, t1, nt)