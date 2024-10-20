import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def goodwill(par, t , v, k, n):
    """Goodwill-Oscillator models
        dx/dt = v1 * K1^n/(K1^n+z^n) - v2 * x/(K2+x)

        dy/dt = v3 * x - v4 * y/(K4+y)

        dz/dt = v5*y - v6 * z/(K6+z)
    """

    x,y,z = par

    dx = v[0] * (k[0]**n / (k[0]**n + z)) - v[1] * (x / (k[1] + x))
    dy = v[2] * x - v[3] * ( y / (k[2] + y))
    dz = v[4] * y - v[5] * (z / (k[3] + z))

    return [dx, dy, dz]



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
        
    def goodwill_solver(self):

        t = self.t
        par = self.par
        v = self.v
        k = self.k
        n = self.n

        return odeint(goodwill, par, t, args = (v, k , n))






par = [0,0,0]
v = [0.7, 0.45, 0.7, 0.35, 0.7, 0.35]
k = [1,1,1,1]
n = 7
t = np.arange(0,1000, 0.01)

good = Goodwill_models(par, v, k, n, t)

z = good.goodwill_solver()
print(z)

plt.plot(t,z[:,0],'b-',label=r'$\frac{dx}{dt}= v_1 \frac{K_1^2}{K_1^n + z^n} - v_2 \frac{x}{K_2 + x}$')
plt.plot(t,z[:,1],'r--',label=r'$\frac{dy}{dt}= v_3x - v_4 \frac{y}{K_4 + y}$')
plt.ylabel('response')
plt.xlabel('time')
plt.legend(loc='best')
plt.show()