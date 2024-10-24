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
    v1, v2, v3, v4, v5, v6 = v
    k1,k2,k4,k6 = k

    dx = (v1 * (k1**n / (k1**n + z**n))) - (v2 * (x / (k2 + x)))
    dy = (v3 * x) - (v4 * ( y / (k4 + y)))
    dz = (v5 * y) - (v6 * (z / (k6 + z)))

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

        return odeint(goodwill, par, t, args = (v, k, n))
    
    
    def norm_to_mean(self):
        solv = self.goodwill_solver()
        norm = [solv[-12000:,i] / np.mean(solv[-12000:,i]) for i in range(solv.shape[1])]   # normalizing to mean

        return norm


    def goodplot_timeseries(self):

        norm = self.norm_to_mean()
        t = self.t[-12000:]
        
        plt.plot(t,norm[0],'g',label=r'$\frac{dx}{dt}= v_1 \frac{K_1^2}{K_1^n + z^n} - v_2 \frac{x}{K_2 + x}$')
        plt.plot(t,norm[1],'r',label=r'$\frac{dy}{dt}= v_3x - v_4 \frac{y}{K_4 + y}$')
        plt.plot(t,norm[2],'b',label=r'$\frac{dz}{dt}= v_5y - v_6 \frac{z}{K_6 + z}$')
        plt.ylabel('concentraition [a.u.]')
        plt.ylim(0,5)
        plt.xlim(t[0],t[-1])
        plt.xlabel('time [h]')
        plt.legend(loc='best')
        plt.show()

        return None


    def phasespace(self):
        norm = self.norm_to_mean()

        plt.subplot(3, 1, 1)
        plt.plot(norm[0],norm[1],'g')
        plt.ylabel('[y] [a.u.]')
        plt.xlabel('x concentraition [a.u.]')
        plt.ylim(0,3)
        plt.xlim(0,5)
        plt.title("Phasespace")

        plt.subplot(3, 1, 2)
        plt.plot(norm[0],norm[2], 'r')
        plt.ylabel('[z] [a.u.]')
        plt.xlabel('x concentraition [a.u.]')
        plt.ylim(0,3)
        plt.xlim(0,5)

        plt.subplot(3, 1, 3)
        plt.plot(norm[1],norm[2], 'b')
        plt.ylabel('[z] [a.u.]')
        plt.xlabel('y concentraition [a.u.]')
        plt.ylim(0,3)
        plt.xlim(0,5)

        plt.show()

        return None
    

    def bifurcation_values(self, v_start : int, v_end : int, v_index : int, par_index : int):
        """getting max and min of our solution

        Args:
            v_start (int): Start
            v_end (int): End
            v_index (int) : index for which v will be look at
            par_index (int) : index for which parameter
        """

        t = self.t
        par = self.par
        k = self.k
        n = self.n
        v_look = np.arange(v_start, v_end, 0.01)
        maxi = []
        mini = []
        v = self.v
        v_new = []
        for i in range(len(v_look)):
            v[v_index] = v_look[i]
            v_new.append(v.copy())  #.copy() prevent overrighting the list with the new variable

        solve = [odeint(goodwill, par, t, args = (o, k, n)) for o in v_new]
        
        normalize = lambda x: [x[-12000:, j] / np.mean(x[-12000:, j]) for j in range(3)]

        norm = [normalize(i) for i in solve]

        maxi = [max(i[0]) for i in norm]
        mini = [min(i[0]) for i in norm]
        
        return maxi, mini

    
    def bifurcation_plot(self, v_start : int, v_end : int, v_index : int, par_index : int):
        maxi, mini = self.bifurcation_values(v_start, v_end,v_index, par_index)
        v_look = np.arange(v_start, v_end, 0.01)
        v = ["v$_1$", "v$_2$", "v$_3$", "v$_4$", "v$_5$", "v$_6$", "v$_7$"]
        plt.plot(v_look,maxi,'g')
        plt.plot(v_look,mini,'g')
        if par_index == 0 :
            plt.ylabel('x$_{min}$, x$_{max}$')
            plt.ylim(0,6)
            plt.xlim(0,v_end)
            label = "x rate by changing " + v[v_index]
            plt.xlabel(label)
        
        elif par_index == 1:
            plt.ylabel('y$_{min}$, y$_{max}$')
            plt.ylim(0,6)
            plt.xlim(0,v_end)
            label = "y rate by changing " + v[v_index]
            plt.xlabel(label)
        
        else:
            plt.ylabel('z$_{min}$, z$_{max}$')
            plt.ylim(0,6)
            plt.xlim(0,v_end)
            label = "z rate by changing " + v[v_index]
            plt.xlabel(label)


        plt.show()

        return None






par = [0,0,0]
v = [0.7, 0.45, 0.7, 0.35, 0.7, 0.35]
k = [1,1,1,1]
n = 7
t = np.arange(0,500, 0.01) # dont set time at 0. there will be some transient effects on the oscillation

good = Goodwill_models(par, v, k, n, t)


# [examples, timeseries and phasespace]_______________________________________________________________________________________________________________________


solv = good.goodplot_timeseries()
print(solv, good.phasespace())


# [examples, bifurcation]_______________________________________________________________________________________________________________________

print(good.bifurcation_plot(0.01,1.5, 1, 0))

# there is some damping issues and some min and max issues..

