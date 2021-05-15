#!/usr/bin/env python
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# This is just for demonstration of the simulation on a much smaller scale.

# Inputs.
N = 100
print("Total Population           =   "+ str(N))
Io = 1
print("Infected population        =   " + str(Io));
Ro = 0
Do = 0
Vo = 0
print("Removed population         =   " + str(Ro));
So = N-Io-Ro-Vo
print("Susceptible population     =   " + str(So));

infection_rate = .1
#infection_rate = 0.09

r = infection_rate*5
print("Infection probability (r)  =   " + str(r))

y = 1/7
print("Removal probability (y)    =   " + str(y))
u = .25
print("Mortality probability      =   " + str(u))
print()

t = np.linspace(0, 210, 211)

def v(time):
    #return 0
    return 0 if time < 32 or time > 125 else .2

def c(time):
    #return 5
    return 5 if time < 25 or time > 60 else .5

def newr(time):
    return c(time) * infection_rate

# This function is the actual mathematical model.
def sirdsv(y, t, N, beta, gamma, alpha, rho, m, q, z):
    S, I, R, D, V = y
    dSdt = (-newr(t) * S * I / N) + (m*R) - (z*v(t)*S)
    dIdt = (newr(t) * S * I / N) - (1 - alpha)*gamma*I - alpha*rho*I
    dRdt = ((1 - alpha) * gamma * I) - (m*R)
    dDdt = alpha * rho * I
    dVdt = z*v(t)*S
    return dSdt, dIdt, dRdt, dDdt, dVdt

initials = So, Io, Ro, Do, Vo
ret = odeint(sirdsv, initials, t, args=(N, r, y, u, 1/10, 1/30, 1/19, 1/14))
S, I, R, D, V = ret.T

print("I: " + str(I))
print("D: " + str(D))
print("V: " + str(V))

# Plotting the data.
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
ax.plot(t, S, 'b', alpha=0.5, lw=2, label='Susceptible')
ax.plot(t, I, 'r', alpha=0.5, lw=2, label='Infected')
ax.plot(t, R, 'g', alpha=0.5, lw=2, label='Temporary Immunity')
ax.plot(t, D, 'k', alpha=0.5, lw=2, label='Deceased')
ax.plot(t, V, 'c', alpha=0.5, lw=2, label='Vaccinated')
ax.set_xlabel('Time (days)')
ax.set_ylabel('Number')
ax.set_ylim(0,100)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.show()
