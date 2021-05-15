#!/usr/bin/env python
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from datareadtest import avg_infect_rate, avg_mort_rate, avg_vac_rate

# This file is for testing the accuracy of the model. It takes the known inputs from February 15th
# and runs the simulation, then it compares the actual results from April 15th to the outputted results.

# Inputs for February 15th.
N = 331002647
Io = 938062
Ro = 4074388
Do = 0
Vo = 15015434
So = N-Io-Ro-Vo

infection_rate = float(avg_infect_rate)

r = infection_rate*1

y = 1/10
u = float(avg_mort_rate)

t = np.linspace(0, 54, 55)

# This function is the actual mathematical model.
def sirdsv(y, t, N, beta, gamma, alpha, rho, m, q, z):
    S, I, R, D, V = y
    dSdt = (-beta * S * I / N) + (m*R) - (z*q*S)
    dIdt = (beta * S * I / N) - (1 - alpha)*gamma*I - alpha*rho*I
    dRdt = ((1 - alpha) * gamma * I) - (m*R)
    dDdt = alpha * rho * I
    dVdt = z*q*S
    return dSdt, dIdt, dRdt, dDdt, dVdt

initials = So, Io, Ro, Do, Vo
ret = odeint(sirdsv, initials, t, args=(N, r, y, u, 1/10, 1/30, 0.051, 1/14))
S, I, R, D, V = ret.T

print("-------------------------------------------------")

print("Simulated infected population:       " + str(I[54]))
print("Expected/Actual infected population: 623753")
print("Percent error: " + str(((623753-591159)/623753)*100) + "\n")

print("Simulated deceased population:       " + str(D[54]))
print("Expected/Actual deceased population: 81495")
print("Percent error: " + str(((81495-79143)/81495)*100) + "\n")

print("Simulated vaccinated population:       " + str(V[54]))
print("Expected/Actual vaccinated population: 70692645")
print("Percent error: " + str(((70715115-70692645)/70692645)*100))
