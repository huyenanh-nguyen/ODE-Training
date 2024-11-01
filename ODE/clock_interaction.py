import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.signal import argrelmax
from scipy.signal import find_peaks

# [Clock-interactions with their Enviroment]_________________________________________________________________________________________________________________________________________________-

def meanfield(n, x):
    """there is a coupling mechanism between the neurons through periodic neurotransmitter release and synaptic connections./n
    Global coupling among all oscillators in the SCN (suprachiasmatic nucleus can be achieved through the mean-field M, 
    wich can be defined as the average concentration of Neurotransmitter x:/n

    M = 1/N ∑ x_i (From i = 1 to N)

    Args:
        n (int): Numbers of neurotransmitter
        x (list or array): List of the concentration of the neurotransmitter.

    Returns:
        float: average concentration of the neurotransmitter x_i
    """
    x_sum = x[0]
    for i in range(1, n):
        x_sum += x[i]
    
    return x_sum/n


def heterogeneous_oscillator(par, t, A, period, lam):
    """
    for heterogenus amplitudephase oscillators without a coupling-term.

    Args:
        par (list): x and y values as list
        t (array): time
        A (int): Oscillation amplitude
        period (list or array): period
        lam (int): amplitude relaxtation rate

    Returns:
        ODE
    """
    x, y = par

    dx = lam * x * (A - np.sqrt(x**2 + y**2)) - (2 * np.pi / period) * y

    dy = lam * y *(A - np.sqrt(x**2 + y**2)) + (2 * np.pi / period) * x

    return [dx, dy]


def coupled_oscillator(par, t, A, period, K, n, lam):
    """
    K * Meanfield = Z(t) = F * cos(2*π/T * t + phi) -> Zeitgeber function that drives an autonomous system (drives oscillator of x -> forcing term)
    So the Oscillator get coupled by the mean-field M.

    Args:
        par (list): x and y values as list
        t (array or list): time
        A (int): Oscillation amplitude
        period (int): period
        K (int): denotes strength of the coupling between meanfield and single oscillatory units
        n (int): numbers of values of x in the area
        lam (int): amplitude relaxtation rate

    Returns:
        ODE
    """
    x, y = par

    dx = lam * x * (A - np.sqrt(x**2 + y**2)) - (2 * np.pi / period) * y + K * meanfield(n, x)

    dy = lam * y *(A - np.sqrt(x**2 + y**2)) + (2 * np.pi / period) * x

    return [dx, dy]



class Clock_Interaction:

    def __init__(self, par, t, A, period, lam, n):
        """_summary_

        Args:
            par (_type_): _description_
            t (_type_): _description_
            A (_type_): _description_
            period (_type_): _description_
            lam (_type_): _description_
            n (int): numbers of x values
        """
        self.par = par
        self.t = t
        self.A = A
        self.period = period
        self.lam = lam
        self.n = n 

print(meanfield(3,[1,3,5,4]))