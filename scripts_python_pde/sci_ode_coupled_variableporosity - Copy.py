'''Solve lumped parameter model using scipy ode module
'''

import scipy.integrate
import matplotlib.pyplot as pyplot
import numpy
import iapws

def odes(t, y, flows, water, rock, P0, T0):
    '''Mass and energy conservation equations
       allow for variable porosity
       phi = phi0 * (1 + cr*(p - p0) - beta*(T - T0))
    '''
    T = y[0]
    P = y[1]

    '''parameters for dTdt equation
    '''
    Wr = flows.Wr
    W_p = flows.ProdRate(t)
    W_inj = flows.InjRate(t)
    W = W_p - W_inj

    R = W_inj * flows.h_inj
    k = W_p * flows.h_p
    
    # update phi
    phi = rock.phi * (1 + rock.c*(P - P0) + rock.beta*(T - T0))

    B = ((1-phi)*rock.rho*rock.C*rock.V) + (rock.V*phi*water.rho*water.C)
    
    Sm = rock.V * phi * water.rho * water.c

    dTdt = (R - k)/B
    dPdt = (Wr-W)/Sm

    if (t > flows.t1):
        # dummy statement
        dum = 1

    return numpy.array([dTdt, dPdt])


class RockParamsClass(object):
    def __init__(self, phi, rho, C, V, c, beta):
        self.phi = phi
        self.rho = rho
        self.C = C
        self.V = V
        self.c = c
        self.beta = beta


class WaterParamsClass(object):
    def __init__(self, rho, C, c):
        self.rho = rho
        self.C = C
        self.c = c
    
    def RhoC(self,P,T):
        state = iapws.IAPWS97(P=P/10e6, T=T+273.15)
        rho = state.rho
        self.rho = rho


class FlowParamsClass(object):
    def __init__(self, W_p, h_p, W_inj, h_inj, Wr, t1, t2):
        self.W_p = W_p
        self.h_p = h_p
        self.W_inj = W_inj
        self.h_inj = h_inj
        self.Wr = Wr
        self.t1 = t1
        self.t2 = t2

    def ProdRate(self, t):
        if (t < self.t1):
            return self.W_p
        elif (t < self.t2):
            return 0.0
        else:
            return self.W_p

    def InjRate(self, t):
        if (t < self.t1):
            return self.W_inj
        elif (t < self.t2):
            return 0.0
        else:
            return self.W_inj


if __name__ == "__main__":

    # Parameters for equations

    # rock properties
    phi = 0.2
    rho_r = 2650
    C_r = 1000
    V = 1e7
    cr = 1.33e-9
    beta = 0.0

    # water properties
    C_w = 4200
    P0 = 50.0e5
    P=P0
    dP=1.0e3
    T=25.0
    state=iapws.IAPWS97(P=P/1.0e6, T=T+273.15)
    rho = state.rho
    c = state.c

    
    # flow rates
    Wr = 0

    W_inj = 15
    h_inj = 255334 
    W_p = 20
    h_p = 592216

    T0 = 140.0
    P0 = 50.0e5
    P=P0

    t1 = 864000
    t2 = 2*t1
    t3 = 3*t1
    tstep = 1.0


    params = (FlowParamsClass(W_p, h_p, W_inj, h_inj, Wr, t1, t2), WaterParamsClass(rho, C_w, c),
                RockParamsClass(phi, rho_r, C_r, V, cr, beta), P0, T0)

    dt = numpy.array([0, t3])
    times = numpy.arange(dt[0], dt[1], tstep)
    y0 = numpy.array([T0, P0])

    soln = scipy.integrate.solve_ivp(odes, dt, y0, method='BDF', t_eval=times, args=params)
    t = soln.t
    T = soln.y[0]
    print(T)
    P = soln.y[1]
    print(P*1e-5)

    fig, ax = pyplot.subplots(2)

    ax[0].plot(t*1.157407e-5, T, label='T')
    ax[0].set(ylim=(139.5, 140))
    ax[1].plot(t*1.157407e-5, P*1e-5, label='P')
    pyplot.legend()
    pyplot.show()
