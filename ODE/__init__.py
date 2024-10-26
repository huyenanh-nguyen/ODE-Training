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

The inital parameters are -> par, t, v, k, n, t_step, t_last:
Args:
    par (ndarray or list): x, y, z values. Initial values
    t (ndarray or list): timespan
    v (ndarray or list): produktions or degradtionsrate for v1, v2, v3, v4, v5, v6
    k (ndarray or list): half-saturated constante -> K1, K2, K4, K6
    n (int): Hill coefficient
    t_step (float or int): if we choose a time from 0 to 5000, how many steps should the system take till it reach 5000
    t_last (int): because the system has to go through transient phase until it reachs his equilibrium. \n
                    So we need to remove the first part of the solution in order to see a stable plot.\n
                    We are only taking the last couple of for example 1000 timepoints in count.\n
"""


from .goodwin import Goodwin