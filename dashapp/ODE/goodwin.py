import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.signal import argrelmax
from scipy.signal import find_peaks


def goodwin(par , t , v , k , n : int):
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

def goodwin_with_positive_loop(par , t , v , k , n : int, c : int):
    """Goodwill-Oscillator models with a positive feedbackloop on the systemvariable x
        dx/dt = v1 * (K1^n + c * x)/(K1^n+z^n) - v2 * x/(K2+x)

        dy/dt = v3 * x - v4 * y/(K4+y)

        dz/dt = v5*y - v6 * z/(K6+z)

        c (int): positive feedback loop on x
    """

    x,y,z = par
    v1, v2, v3, v4, v5, v6 = v
    k1,k2,k4,k6 = k

    dx = (v1 * (k1**n / (k1**n + z**n)) * (1 + c*x))- (v2 * (x / (k2 + x)))
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
    

    def goodwin_period(self, par_index : int):
        """
        Getting Period T of the Goodwin-Oscillation.

        Args:
            par_index (int): index of the choosen system (x -> 0, y -> 1, z -> 2)

        Returns:
            int: period of the oscillation
        """
        norm = self.goodwin_normalizer()[par_index]
        maxi = argrelmax(norm)[0]   # returning the index of the maximum

        t = self.t

        diff_t = t[maxi[1]] - t[maxi[0]] 

        return diff_t
    

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
        plt.ylim(np.min(norm) - 0.1, np.max(norm) + 0.5)
        plt.xlim(left = 0)
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
    

    def v_change(self, v_start : float, v_end : float, v_step : float, v_index : int):
        """
        For the bifurcation part, we want to change one of the control parameters. In this case, we want to change the v-parameters.
        The v_index gives the position of the v-value that will be adjusted.
        v_start and v_end give us the intervals, and v_step gives us the number of steps to reach the end of the intervals.

        Args:
            v_start (float): First value of the interval
            v_end (float): Last value of the interval
            v_step (float): Steps of the interval
            v_index (int): Position of the v-value that will be changed (v1 -> 0, v2 -> 1, v3 -> 2, v4 -> 3, v5 -> 4, v6 -> 5)

        Returns:
            List: A list of the v_array
        """
        v = self.v
        v_change = np.arange(v_start, v_end, v_step)
        v_new = []

        for i in v_change:
            v[v_index] = i
            v_new.append(v.copy())  #.copy() prevent overrighting the list with the new variable
        
        return v_new


    def bifurcation_solver(self, v_start : float, v_end : float, v_step : float, v_index : int):
        """
        Args:
            v_start (float): First value of the interval
            v_end (float): Last value of the interval
            v_step (float): Steps of the interval
            v_index (int): Position of the v-value that will be changed (v1 -> 0, v2 -> 1, v3 -> 2, v4 -> 3, v5 -> 4, v6 -> 5)

        Returns:
            List: changing one v_parameters and solve the ODE (Goodwin)
        """
        v = self.v_change(v_start, v_end, v_step, v_index)
        par = self.par
        t = self.t
        k = self.k
        n = self.n

        sol = [odeint(goodwin, par, t, args= (i, k, n)) for i in v]

        return sol
    

    def bifurcation_normalizer(self, v_start : float, v_end : float, v_step : float, v_index : int):
        """
        Args:
            v_start (float): First value of the interval
            v_end (float): Last value of the interval
            v_step (float): Steps of the interval
            v_index (int): Position of the v-value that will be changed (v1 -> 0, v2 -> 1, v3 -> 2, v4 -> 3, v5 -> 4, v6 -> 5)

        Returns:
            List: normalized values with the order: [numbers of changed v_parameters][datapoints] x,y,z - Parameters]
        """
        sol = self.bifurcation_solver(v_start, v_end, v_step, v_index)
        t_step = self.t_step
        t_last = self.t_last
        keep = int(t_last/t_step)
        par = self.par

        norm = []

        for i in range(len(sol)):
            v_holder = []
            for k in range(len(par)):
                x = sol[i][- keep:, k] / np.mean(sol[i][-keep:,k])   # normalizing to mean
                v_holder.append(x)
            norm.append(v_holder)

       
        return norm
    

    def bifurkacation_normalizier_plot(self, v_start : float, v_end : float, v_step : float, v_index : int):
        """_summary_

        Args:
            v_start (float): First value of the interval
            v_end (float): Last value of the interval
            v_step (float): Steps of the interval
            v_index (int): Position of the v-value that will be changed (v1 -> 0, v2 -> 1, v3 -> 2, v4 -> 3, v5 -> 4, v6 -> 5)

        Returns:
            plot: plotting all systems in one plot
        """

        norm = self.bifurcation_normalizer(v_start, v_end, v_step, v_index)
        t_step = self.t_step
        t_last = self.t_last

        t = np.arange(0, t_last, t_step)

        for i in range(len(norm)):
            plt.plot(t,norm[i][0],'g',label=r'$\frac{dx}{dt}= v_1 \frac{K_1^2}{K_1^n + z^n} - v_2 \frac{x}{K_2 + x}$')
            plt.plot(t,norm[i][1],'r',label=r'$\frac{dy}{dt}= v_3x - v_4 \frac{y}{K_4 + y}$')
            plt.plot(t,norm[i][2],'b',label=r'$\frac{dz}{dt}= v_5y - v_6 \frac{z}{K_6 + z}$')
        plt.ylabel('concentraition [a.u.]')
        plt.ylim(0,30)
        plt.xlim(0, t[-1])
        plt.xlabel('time [h]')
        plt.legend(loc='best')
        plt.show()
        
        return None
    

    def bifurcation_extrema(self,  v_start : float, v_end : float, v_step : float, v_index : int):
        """
        Args:
            v_start (float): First value of the interval
            v_end (float): Last value of the interval
            v_step (float): Steps of the interval
            v_index (int): Position of the v-value that will be changed (v1 -> 0, v2 -> 1, v3 -> 2, v4 -> 3, v5 -> 4, v6 -> 5)

        Returns:
            list: returning two lists. first one contains all Maxima from the Goodwin-Oscillation and the second one all Minima from the Goodwin-Oscillation
        """
        norm = self.bifurcation_normalizer(v_start, v_end, v_step, v_index)
        par = self.par

        maxi = []
        mini = []
        for i in range(len(norm)):
           
            maxi.append([max(norm[i][k]) for k in range(len(par))])
            mini.append([min(norm[i][k])for k in range(len(par))])

        return maxi, mini
    

    def bifurcation_maxima_index(self,  v_start : float, v_end : float, v_step : float, v_index : int):
        """
        Args:
            v_start (float): First value of the interval
            v_end (float): Last value of the interval
            v_step (float): Steps of the interval
            v_index (int): Position of the v-value that will be changed (v1 -> 0, v2 -> 1, v3 -> 2, v4 -> 3, v5 -> 4, v6 -> 5)

        Returns:
            list: list with all the Maxima_index for the systemparameters x,y,z. The distance varies a bit because this model is a non linear dynamical oscillator with errors and the parameters get changed a lot here.
        """
        norm = self.bifurcation_normalizer(v_start, v_end, v_step, v_index)
        par = self.par

        maxi = []
        for i in range(len(norm)):
            maxi.append([find_peaks(norm[i][k])[0] for k in range(len(par))])

        return maxi
    

    def bifurkation_plot(self, v_start : float, v_end : float, v_step : float, v_index : int, par_index : int):
        """
        Showing the Bifurkation behavior by changing the parameters and in which system
        Args:
            v_start (float): First value of the interval
            v_end (float): Last value of the interval
            v_step (float): Steps of the interval
            v_index (int): Position of the v-value that will be changed (v1 -> 0, v2 -> 1, v3 -> 2, v4 -> 3, v5 -> 4, v6 -> 5)
            par_index (int): Position of the System-value that we want to plot (x -> 0, y -> 1, z -> 2)

        Returns:
            Plot: Bifurcation diagrams of the Goodwin model as a function of the systemparameters x,y,z degradation rate ν
        """

        maxi = self.bifurcation_extrema(v_start, v_end,v_step, v_index)[0]
        mini = self.bifurcation_extrema(v_start, v_end,v_step, v_index)[1]
        v_look = np.arange(v_start, v_end, v_step)

        v = ["v$_1$", "v$_2$", "v$_3$", "v$_4$", "v$_5$", "v$_6$", "v$_7$"]

        plt.plot(v_look, np.array(maxi)[:,par_index],'g')
        plt.plot(v_look, np.array(mini)[:,par_index],'g')
        
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
            plt.xlim(0, v_end)
            label = "z rate by changing " + v[v_index]
            plt.xlabel(label)


        plt.show()

        return None
    

    def bifurkation_period(self, v_start : float, v_end : float, v_step : float, v_index : int, par_index : int):
        """
        Args:
            v_start (float): First value of the interval
            v_end (float): Last value of the interval
            v_step (float): Steps of the interval
            v_index (int): Position of the v-value that will be changed (v1 -> 0, v2 -> 1, v3 -> 2, v4 -> 3, v5 -> 4, v6 -> 5)
            par_index (int): Position of the System-value that we want to plot (x -> 0, y -> 1, z -> 2)

        Returns:
            List: Periods for choosen systemparameters and choosen parameter that get changed. We are getting the mean of the distance, because the dinamic of this oscillator is nonlinear
        """
        maxi_index = self.bifurcation_maxima_index(v_start, v_end,v_step, v_index)

        t_last = self.t_last
        t_step = self.t_step

        t = np.arange(0, t_last, t_step)

        period = []

        for i in range(len(maxi_index)):
            diff_t = np.diff(t[maxi_index[i][par_index]])
            period.append(np.mean(diff_t))
        
        return period
    

    def period_dynamic_plot(self, v_start : float, v_end : float, v_step : float, v_index : int, par_index : int):
        period = self.bifurkation_period(v_start, v_end,v_step, v_index, par_index)
        v = np.arange(v_start, v_end, v_step)
        par = ["x", "y", "z"]

        valid_indices = ~np.isnan(period)

        v = v[valid_indices]
        period = np.array(period)[valid_indices]




        plt.plot(v, period,'g')
        plt.ylabel('Period [h]')
        plt.ylim(0,(period.max()+10))
        plt.xlim(0, v_end)
        label = par[par_index] + ' degration rate'
        plt.xlabel(label)
        plt.legend(loc='best')
        plt.show()

        return None
    

    def goodwin_positive_feedback(self, c : int):

        par = self.par
        t = self.t
        v = self.v
        k = self.k
        n = self.n
        
        return odeint(goodwin_with_positive_loop, par, t, args=(v, k , n, c))
    
    def goodwin_positive_feedback_normalizier(self, c : int):
        sol = self.goodwin_positive_feedback(c)

        t_step = self.t_step
        t_last = self.t_last

        keep = int(t_last / t_step)

        norm = [sol[- keep:,i] / np.mean(sol[-keep:,i]) for i in range(sol.shape[1])]   # normalizing to mean
        
        return norm

    def limitcircle_timeseries_positive_feedback(self, c : int):
            """
            Plotting the solution of the Goodwin differentiantion equation, which got normalize to their mean.

            Returns:
                Plot: shows a limit circle oscillation as time series. (keeping the last timepoints)
            """

            norm = self.goodwin_positive_feedback_normalizier(c)
            t_step = self.t_step
            t_last = self.t_last

            t = np.arange(0, t_last, t_step)

            plt.plot(t,norm[0],'g',label=r'$\frac{dx}{dt}= (v_1 \frac{K_1^2}{K_1^n + z^n}) \cdot (1 + cx)- v_2 \frac{x}{K_2 + x}$')
            plt.plot(t,norm[1],'r',label=r'$\frac{dy}{dt}= v_3x - v_4 \frac{y}{K_4 + y}$')
            plt.plot(t,norm[2],'b',label=r'$\frac{dz}{dt}= v_5y - v_6 \frac{z}{K_6 + z}$')
            plt.ylabel('concentraition [a.u.]')
            plt.ylim(np.min(norm) - 0.1, np.max(norm) + 0.5)
            plt.xlim(left = 0)
            plt.xlabel('time [h]')
            plt.legend(loc='best')
            plt.show()

            return None


        
    
    


    