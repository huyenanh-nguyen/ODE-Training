import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import matplotlib.gridspec as gridspec
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
                          We are only taking the last couple of for example 1000 timepoints in count.\n
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
        Also, i am removing the transiente part and only allow the last couple timepoints.

        Returns:
            array: Oscillations were normalized to their mean
        """
       
        sol = self.goodwin_solver()
        t_step = self.t_step
        t_last = self.t_last

        keep = int(t_last / t_step)

        norm = [sol[- keep:,i] / np.mean(sol[-keep:,i]) for i in range(sol.shape[1])]   # normalizing to mean
        
        return norm
    

    def limitcircle_timeseries(self):
        """
        Plotting the solution of the Goodwin differentiantion equation, which got normalize to their mean.

        Returns:
            Plot: shows a limit circle oscillation as time series. (keeping the last timepoints)
        """

        norm = self.goodwin_normalizer()
        t_step = self.t_step
        t_last = self.t_last

        t = np.arange(0, t_last, t_step)

        plt.plot(t,norm[0],'g',label=r'$\frac{dx}{dt}= v_1 \frac{K_1^2}{K_1^n + z^n} - v_2 \frac{x}{K_2 + x}$')
        plt.plot(t,norm[1],'r',label=r'$\frac{dy}{dt}= v_3x - v_4 \frac{y}{K_4 + y}$')
        plt.plot(t,norm[2],'b',label=r'$\frac{dz}{dt}= v_5y - v_6 \frac{z}{K_6 + z}$')
        plt.ylabel('concentraition [a.u.]')
        plt.ylim(0,5)
        plt.xlim(0, t[-1])
        plt.xlabel('time [h]')
        plt.legend(loc='best')
        plt.show()

        return None
    

    def limitcircle_phasespace(self):

        norm = self.goodwin_normalizer()
        fig, ax = plt.subplots(3, 1, figsize=(4, 8), sharex = False, sharey = False)
        fig.suptitle("Phasespace")
        ax[0].plot(norm[0], norm[1])
        ax[0].set_xlabel('x concentraition [a.u.]')
        ax[0].set_ylabel('y concentraition [a.u.]')

        ax[1].plot(norm[1], norm[2], "r")
        ax[1].set_xlabel('y concentraition [a.u.]')
        ax[1].set_ylabel('z concentraition [a.u.]')

        ax[2].plot(norm[0], norm[2], "g")
        ax[2].set_xlabel('x concentraition [a.u.]')
        ax[2].set_ylabel('z concentraition [a.u.]')

        plt.tight_layout()  # avoinding overlapping the figures
        
        plt.show()

        return None



        
    
    


    