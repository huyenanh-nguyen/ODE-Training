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

    Trying to recreate the figures in Marta del Olmos paper. There are about the Goodwin model. 
    She described more than the Goodwin Model, so that is why i called this class the Goodwin-class.

    A 3-Parameter System, where X activates Y and Y activates Z and Z inhibits X, can be descriebed through the 
    Goodwin model:

        dx/dt = v1 * K1^n/(K1^n+z^n) - v2 * x/(K2+x)

        dy/dt = v3 * x - v4 * y/(K4+y)

        dz/dt = v5*y - v6 * z/(K6+z)
    """

    
    def __init__(self, par, t, v, k, n):
        """Goodwill-Oscillator models
        dx/dt = v1 * K1^n/(K1^n+z^n) - v2 * x/(K2+x)

        dy/dt = v3 * x - v4 * y/(K4+y)

        dz/dt = v5*y - v6 * z/(K6+z)

        Args:
            par (_type_): _description_
            t (_type_): _description_
            v (_type_): _description_
            k (_type_): _description_
            n (_type_): _description_
        """