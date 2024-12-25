import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.signal import argrelmax
from scipy.signal import find_peaks

def duffing(par, t, gamma, alpha, omega):
    x, y, z = par

    dx = (y)
    dy = (-x - x**3 - gamma * y + alpha * np.cos( 2 * np.pi * z))
    dz = (omega / (2 * np.pi))

    return [dx, dy, dz]

# [Duffing]________________________________________________________________________________________________________________________________________
class Duffing:
    def __init__(self, par, t, gamma, alpha, omega):
        self.par = par
        self.t = t
        self.gamma = gamma
        self.alpha = alpha
        self.omega = omega

    
    def duffing_solver(self):
        par = self.par
        t = self.t
        gamma = self.gamma
        alpha = self.alpha
        omega = self.omega

        sol = odeint(duffing, par, t, args = (gamma, alpha, omega))

        return sol
    

    def x_solv(self, keep):
        """only showing the x solutions

        Args:
            keep (int): last couple of timepoints that we want to see
        """
        sol = self.duffing_solver()

        x_solv = sol[-keep:,0]

        return x_solv
    

    def y_solv(self, keep):
        """only showing the y solutions

        Args:
            keep (int): last couple of timepoints that we want to see
        Returns:
            Array: 1D Array of the Y-Solution
        """
        sol = self.duffing_solver()

        y_solv = sol[-keep:,1]

        return y_solv
    

    def z_solv(self, keep):
        """only showing the 2 solutions

        Args:
            keep (int): last couple of timepoints that we want to see
        Returns:
            Array: 1D Array of the 2-Solution
        """
        sol = self.duffing_solver()

        z_solv = sol[-keep:,2]

        return z_solv


# par = [-2,-2,-2]
# t_step = 0.01
# t_last = 500 # 50h -> 1 point represent 1h
# t = np.arange(0, 5000, t_step)
# keep = int(t_last / t_step)

# gamma = 0.2
# alpha = 2.5
# omega = 0.36

# sol = odeint(duffing, par, t, args= (gamma, alpha, omega))
# x_sol = sol[keep:,0]
# y_sol = sol[keep:,1]

# label = r"$\gamma$ = " + str(gamma) + "\n" + r"$\alpha$ = " + str(alpha) + "\n" + r"$\omega$ = " + str(omega)

# plt.plot(x_sol,y_sol,'g', label = label)
# plt.ylabel('y')
# plt.ylim(np.min(y_sol) - 0.1, np.max(y_sol) + 0.5)
# plt.xlim(np.min(x_sol) - 0.1, np.max(x_sol) + 0.5)
# plt.legend(loc='best')
# plt.show()


