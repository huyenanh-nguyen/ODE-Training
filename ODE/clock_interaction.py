import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.signal import argrelmax
from scipy.signal import find_peaks
 
# [ODE]___________________________________________________________________________________________________________________________________________________________
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
   
    return  np.sum(x, axis = 0)/n
 
def coupled_oscillator(par, t, A, period, lam, K, n):
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
    x = par[0:n:1]
    y = par [-n::1]
 
    dx = lam * x * (A - np.sqrt(x**2 + y**2)) - (2 * np.pi *y / period) + K * meanfield(n, x)  
 
    dy = lam * y *(A - np.sqrt(x**2 + y**2)) + (2 * np.pi* x / period)
 
    return np.concatenate((dx,dy))

# [Interactions]_________________________________________________________________________________________________________________________________
class Clockinteractions:

    def __init__(self, x, y , t, A, period, lam, n, K):
        self.x = x
        self.y = y
        self.t = t
        self.A = A
        self.period = period
        self.lam = lam
        self.n = n
        self.K = K

    def sync_oscillator_solver(self):
        """Solving the coupled Oscillator ODE

        Returns:
            Array: [[x,y], [x,y], [x,y]...]
        """
        x = self.x
        y = self.y
        t = self.t
        A = self.A
        period = self.period
        lam = self.lam
        n = self.n
        K = self.K

        par = np.hstack((x,y))

        sol = odeint(coupled_oscillator, par, t, args = (A, period, lam, K, n))
        return sol
    
    def meanevents(self, value_index):
        """

        Args:
            value_index (int): Solutionposition -> x has the index 0 and y has the index 1

        Returns:
            Array: the mean value for through all the events.
        """
        sol = self.sync_oscillator_solver()
        if value_index == 0:
            mean_event = np.mean(sol.T[0:n:1], axis = 0)
        
        elif value_index == 1:
            mean_event = np.mean(sol.T[-n::1], axis = 0)

        return mean_event


# [Parameter]_____________________________________________________________________________________________________________________________________________________________
 
n = 10  # numbers of events
x = [np.random.uniform(-1,1) for i in range(n)] # x-values
y = [np.random.uniform(-1,1) for i in range(n)] # y-values
 
t_step = 0.1
t_last = 2400 # 50h -> 1 point represent 1h
t = np.arange(0, 100*24, t_step)
 
keep = t_last/t_step
 
A = 0.1   # Amplitude
period = np.random.normal(24, 1.5, size = (n,1)).flatten('C')
lam = 0.03
K = 0.2
 
# [Solution for individual and average events]________________________________________________________________________________________________________________________________________________________________
 
# sol = []
# for i in range(n):
#     tau = period[i]
#     par = x[i], y[i]
#     sol.append(odeint(coupled_oscillator, par, t, args = (A, tau, lam, K, n, x)))
 
par = np.hstack((x, y))
sol = odeint(coupled_oscillator, par, t, args = (A, period, lam, K, n))
 
# sol got two variables x and y. If i go through the list,the list looks like this: [[x,y], [x,y], [x,y]...]
mean_event = np.mean(sol.T[0:n:1], axis = 0)[-int(keep):]    # average of the events
# breakpoint()
# [Plot]______________________________________________________________________________________________________________________________________________________________________________________________________
 
# breakpoint()
 
# plt.plot(np.arange(0, t_last, t_step), np.array(sol)[0,:,0][-int(keep):], "grey")
for j in range(n):
    plt.plot(np.arange(0, t_last, t_step), sol.T[j][-int(keep):] , "grey")
plt.plot(np.arange(0, t_last, t_step), mean_event, "red")
 
plt.ylim(-4,4)
 
plt.xlabel("time [h]")
plt.show()