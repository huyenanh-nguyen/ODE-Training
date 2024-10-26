from ODE import Goodwin
import numpy as np

"""
Recreating Marta del Olmos paper.
"""


# [Goodwin]____________________________________________________________________________________________________________________________

par = [0, 0, 0]
t_step = 0.01
t_last = 200 # 50h -> 1 point represent 1h
t = np.arange(0, 500, t_step)

v = [0.7, 0.45, 0.7, 0.35, 0.7, 0.35]
k = [1,1,1,1]
n = 7

good = Goodwin(par, t, v, k, n, t_step, t_last)

# [Figure 3]: Limit cycle oscillations, plotted as time series and in phase space

timeseries = good.limitcircle_timeseries()
phasespace = good.limitcircle_phasespace()