'''Solve lumped parameter model using scipy ode module
'''

import scipy.integrate
import matplotlib.pyplot as pyplot
import numpy

def odes(t, y):
    T = y[0]
    P = y[1]
    '''parameters for dTdt equation
    '''
    W_inj = 15
    h_inj = 255300 
    W_p = 20
    h_p = 592216

    R = W_inj*h_inj
    k = W_p*h_p
    
    phi = 0.2
    rho_r = 2650
    C_r = 1000
    V = 1e7
    rho = 924.1646597199999
    C_w = 4200
    
    B = ((1-phi)*rho_r*C_r*V)+(V*phi*rho*C_w)
    

    '''parameters for dPdt equation
    '''
    c = 1.33e-9
    Wr = 0
    W = 5
    Sm = V*phi*rho*c
    


    dTdt = (R - k)/B
    dPdt = (Wr-W)/Sm
    return numpy.array([dTdt, dPdt])

dt = numpy.array([0, 864000])
times = numpy.linspace(dt[0], dt[1], 20)
y0 = numpy.array([140, 50e5])

soln = scipy.integrate.solve_ivp(odes, dt, y0, t_eval=times)
t = soln.t
T = soln.y[0]
print(T)
P = soln.y[1]
print(P*1e-5)

fig, ax = pyplot.subplots(2)

ax[0].plot(t*1.157407e-5, T, label='A')
ax[0].set(ylim=(139.5, 140))
ax[1].plot(t*1.157407e-5, P*1e-5, label='P')
pyplot.legend()
pyplot.show()
