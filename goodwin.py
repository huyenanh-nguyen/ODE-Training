import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.signal import argrelextrema


def goodwin(par, t , v, k, n):
    """Goodwill-Oscillator models
        dx/dt = v1 * K1^n/(K1^n+z^n) - v2 * x/(K2+x)

        dy/dt = v3 * x - v4 * y/(K4+y)

        dz/dt = v5*y - v6 * z/(K6+z)
    """

    x,y,z = par
    v1, v2, v3, v4, v5, v6 = v
    k1,k2,k4,k6 = k

    dx = (v1 * (k1**n / (k1**n + z**n))) - (v2 * (x / (k2 + x)))
    dy = (v3 * x) - (v4 * ( y / (k4 + y)))
    dz = (v5 * y) - (v6 * (z / (k6 + z)))

    return [dx, dy, dz]


# [Marta del Olmo]____________________________________________________________________________________________________

class Goodwin:
    """
    # Goodwin - Mathematical Modeling in Circadian Rhythmicity 

    Trying to recreate the figures in Marta del Olmo's paper. Here we will tackle all figures about the Goodwin model. 
    The other models will get their own classes.

    A 3-Parameter System, where X activates Y, Y activates Z, and Z inhibits X, can be described through the 
    Goodwin model:

        dx/dt = v1 * K1^n/(K1^n + z^n) - v2 * x/(K2 + x)

        dy/dt = v3 * x - v4 * y/(K4 + y)

        dz/dt = v5 * y - v6 * z/(K6 + z)
        
    In this class you will find a couple of functions that contain some kind of Goodwin flavor.
    One of these is solving this equation, and the others are plotting the solution and bifurcation relation.

    Also, I will get to know a lot about the package scipy, which is a great exercise!
    """


    def __init__(self, par, t, v, k, n, t_step, t_last):
        """Goodwill-Oscillator models
        dx/dt = v1 * K1^n/(K1^n+z^n) - v2 * x/(K2+x)

        dy/dt = v3 * x - v4 * y/(K4+y)

        dz/dt = v5*y - v6 * z/(K6+z)

        Args:
            par (array or list): x, y, z values. Initial values
            t (array or list): timespan
            v (array or list): produktions or degradtionsrate for v1, v2, v3, v4, v5, v6
            k (array or list): half-saturated constante -> K1, K2, K4, K6
            n (int): Hill coefficient
            t_step (float or int): if we choose a time from 0 to 5000, how many steps should the system take till it reach 5000
            t_last (int): because the system has to go through transient phase until it reachs his equilibrium. \n
                          So we need to remove the first part of the solution in order to see a stable plot.\n
                          We are only taking the last couple of 1000 timepoints in count. (example number)\n
        """

        self.par = par
        self.t = t
        self. v = v
        self.k = k
        self.n = n
        self.t_step = t_step
        self.t_last = t_last


    def goodwin_solver(self):
        """solving the goodwin equations.

        Returns:
            array: returning all the solutions from a defined timespan
        """
        par = self.par
        t = self.t
        v = self.v
        k = self.k
        n = self.n

        return odeint(goodwin, par, t, args= (v, k, n))
    

    def goodwin_normalizer(self):
        """
        The Solution for each parameters are not at the same spot. normalizing to their mean gives us a nice overlay of every solutions.

        Returns:
            array: Oscillations were normalized to their mean
        """
       
        sol = self.goodwin_solver()
        t = self.t
        t_step = self.t_step
        t_last = self.t_last

        return None


    