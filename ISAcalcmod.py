from math import *

# This is a modified version of my ISACalc assignment to find the density

#Constants
g0 = 9.80665
R = 287

levels = [0,11000,20000,32000,47000,51000,71000,86000]
rate = [-0.0065,0,0.001,0.0028,0,-0.0028,-0.0020]


def CALC(h1):
    # Initial values
    T0 = 288.15
    P0 = 101325
    rho0 = 1.225
    # Gradient functions
    def gradient (T0, P0, rho0, a):
        T1 = T0 + rate[i]*(min(h1, levels[i + 1]) - levels[i])
        P1 = P0*(T1/T0)**(-g0/(rate[i]*R))
        rho1 = P1/(R*T1)

        return(round(T1, 4), round(P1, 4), round(rho1, 6))

    def isothermal (T0, P0, rho0):
        T1 = T0
        P1 = P0*exp(-g0/(R*T1)*(min(h1, levels[i + 1]) - levels[i]))
        rho1 = P1/(R*T1)

        return(round(T1, 4), round(P1, 4), round(rho1, 6))

    #Level check
    i = 0
    while i < 8 and h1 > levels[i]:
        if rate[i] != 0:
            T0, P0, rho0 = gradient(T0, P0, rho0, rate[i])
        else:
            T0, P0, rho0 = isothermal(T0, P0, rho0)
        i += 1

    return(rho0)
