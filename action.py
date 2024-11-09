from ODE import Goodwin
from ODE import Clock_Interaction
import numpy as np
import matplotlib.pyplot as plt

"""
Recreating Marta del Olmos paper.
"""


# [Goodwin]____________________________________________________________________________________________________________________________

par = [0, 0, 0]
t_step = 0.01
t_last = 500 # 50h -> 1 point represent 1h
t = np.arange(0, 50000, t_step)

v = [0.7, 0.45, 0.7, 0.35, 0.7, 0.35]
k = [1,1,1,1]
n = 7

good = Goodwin(par, t, v, k, n, t_step, t_last)


# [Figure 3]: Limit cycle oscillations, plotted as time series and in phase space


# timeseries = good.limitcircle_timeseries()
# phasespace = good.limitcircle_phasespace()



# [Figure 4]: Bifurcation diagrams of the Goodwin model as a function of one of the system and changing one of the parameters

# bifurcation = good.bifurkation_plot(0.1, 1.5, 0.01, 1, 0)

# period = good.period_dynamic_plot(0.1, 1.5, 0.01, 1,0)




# [Figure 5]: A positive feedback loop promotes oscillations in a Goodwin-like motif

n_no_loop = 4

# without_loop = Goodwin(par, np.arange(0, 500, t_step), v, k, n_no_loop, t_step, t_last = 300).limitcircle_timeseries()


# t_positive = Goodwin(par, np.arange(0, 5000, t_step), v, k, n_no_loop, t_step, t_last = 120).limitcircle_timeseries_positive_feedback(c = 1)



# [Clock-Interaction]_______________________________________________________________________________________________________________________

n = 50

x = [np.random.randint(-100,100) for i in range(n)]
y = [np.random.randint(-100,100) for i in range(n)]

# par = [x,y]    # possible value for equation?
t_step = 0.01
t_last = 200 # 50h -> 1 point represent 1h
t = np.arange(0, 5000, t_step)

A = 1
period = np.random.normal(24, 1.5, size = (n,1))
lam = 0.03

print(period[0])

clock = Clock_Interaction(x, y , t, A, period, lam, n = n)


# print(np.mean(clock.coupled_solver(t_last, t_step, 0), axis= 0))
keep = t_last/t_step

plt.plot(np.arange(0,t_last, t_step), np.mean(clock.coupled_solver(t_last, t_step, 0), axis= 0)[-int(keep):,0], 'red')

plt.ylabel('x concentraition [a.u.]')
plt.xlabel("time [h]")
plt.show()



# Simulation of biological oscillators