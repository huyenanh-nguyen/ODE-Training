from ODE import Goodwin
import numpy as np

"""
Recreating Marta del Olmos paper.
"""


# [Goodwin]____________________________________________________________________________________________________________________________

par = [0, 0, 0]
t_step = 0.01
t_last = 500 # 50h -> 1 point represent 1h
t = np.arange(0, 5000, t_step)

v = [0.7, 0.5, 0.7, 0.35, 0.7, 0.35]
k = [1,1,1,1]
n = 7

good = Goodwin(par, t, v, k, n, t_step, t_last)


# [Figure 3]: Limit cycle oscillations, plotted as time series and in phase space


# timeseries = good.limitcircle_timeseries()
# phasespace = good.limitcircle_phasespace()


# [Figure 4]: Bifurcation diagrams of the Goodwin model as a function of one of the system and changing one of the parameters

# bifurcation = good.bifurkation_plot(0.1, 1.5, 0.01, 1, 0)

print(good.period_dynamic_plot(0.1, 1.5, 0.01, 1,0))
