import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint


class Goodwill_models:

    def __init__(self, par, v, k, n, t):
        """_summary_

        Args:
            par (array): x, y, z -> y0
            v (array): v1, v2, v3, v4, v5, v6
            k (array): K1, K2, K4, K6
            n (int): 
            t (array): timespan
        """
        self.par = par
        self.v = v
        self.k = k
        self.n = n
        self.t = t
        

    def goodwill(self):
        """Goodwill-Oscillator models
            dx/dt = v1 * K1^n/(K1^n+z^n) - v2 * x/(K2+x)

            dy/dt = v3 * x - v4 * y/(K4+y)

            dz/dt = v5*y - v6 * z/(K6+z)
        """
        par = self.par
        v = self.v
        k = self.k
        n = self.n

        x = v[0] * (k[0]**n / (k[0]**n + par[2])) - v[1] * (par[0] / (k[1] + par[0]))
        y = v[2] * par[0] - v[3] * ( par[1] / (k[2] + par[1]))
        z = v[4] * par[1] - v[5] * (par[2] / (k[3] + par[2]))

        return [x, y, z]
    

    def goodwill_solver(self):
        par = self.par
        t = self.t
        return odeint(self.goodwill(), par, t, args = [self.v, self.k, self.n])






par = [0,0,0]
v = [0.7, 0.45, 0.7,0.35, 0.7, 0.35]
k = [1,1,1,1]
n = 7
t = np.linspace(0,120)

good = Goodwill_models(par, v, k, n, t)

z = good.goodwill_solver()
print(z)

# plt.plot(t,z[:,0],'b-',label=r'$\frac{dx}{dt}=3 \; \exp(-t)$')
# plt.plot(t,z[:,1],'r--',label=r'$\frac{dy}{dt}=-y+3$')
# plt.ylabel('response')
# plt.xlabel('time')
# plt.legend(loc='best')
# plt.show()