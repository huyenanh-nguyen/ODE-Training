import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint


class Goodwill_models:

    def __init__(self, par, v, k, n):
        """_summary_

        Args:
            par (array): x, y, z
            v (array): v1, v2, v3, v4, v5, v6
            k (array): K1, K2, K4, K6
            n (int): 
        """
        self.par = par
        self.v = v
        self.k = k
        self.n = n
        

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
        v = self.v
        k = self.k
        n = self.n