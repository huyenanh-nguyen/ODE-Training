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
    
    return sum(x)/n


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


def coupled_oscillator(par, t, A, period, lam, K, n, x_total):
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

    dx = lam * x * (A - np.sqrt(x**2 + y**2)) - (2 * np.pi / period) * y + K * meanfield(n, x_total)

    dy = lam * y *(A - np.sqrt(x**2 + y**2)) + (2 * np.pi / period) * x

    return [dx, dy]



class Clock_Interaction:
    """
    Now we want to look into the Clock System. /n
    In this Area we want to understand a coupled and an uncoupled oscillatorsystem. What happend if a forced will get add to  an autonomous system which will become a
    non-autonomous system.
    """

    def __init__(self, x ,y , t, A, period, lam : int, n):
        """_summary_

        Args:
            x (list or array): _description_
            y (list or array): _description_
            t (array): time
            A (int): Amplitude
            period (list or array): period
            lam (int): amplitude relaxtation rate
            n (int): numbers of x values
        """
        self.x = x
        self.y = y
        self.t = t
        self.A = A
        self.period = period
        self.lam = lam
        self.n = n 

    def autonomous_solver(self):
        x = self.x
        y = self.y
        t = self.t
        A = self.A
        period = self.period
        lam = self.lam
        n = self.n

        sol = []

        for i in range(n):
            par = x[i], y[i]
            sol.append(odeint(heterogeneous_oscillator, par, t, args= (A, period[i][0], lam)))

        return sol
    

    def autonomous_plot(self, t_last, t_step):
        sol = self.autonomous_solver()
        t = np.arange(0,t_last, t_step)
        keep = t_last/t_step

        for i in sol:
            plt.plot(t, i[-int(keep):,0], 'gray')

        plt.ylabel('x concentraition [a.u.]')
        plt.xlabel("time [h]")
        plt.show()

        return None
    

    def coupled_solver(self, t_last, t_step, K):
        x = self.x
        y = self.y
        t = self.t
        A = self.A
        period = self.period
        lam = self.lam
        n = self.n

        sol = []
        for i in range(n):
            par = x[i], y[i]
            sol.append(odeint(coupled_oscillator, par, t, args= (A, period[i][0], lam, K, n, x)))

        return sol


    
    def coupled_plot(self, t_last, t_step, K):
        sol = self.coupled_solver(t_last, t_step, K)
        t = np.arange(0,t_last, t_step)
        keep = t_last/t_step

        for i in sol:
            plt.plot(t, i[-int(keep):,0], 'red')

        plt.ylabel('x concentraition [a.u.]')
        plt.xlabel("time [h]")
        plt.show()

        return None



    
