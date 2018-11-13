import os
import numpy as np
import matplotlib.pyplot as plt
import math as m
import sys

# phase transtion
# -----------------------------------------------------------------------------
L = np.array([40, 60, 100, 160])
t = np.loadtxt("results/evolution_L=40.txt", usecols=0)

E = []
M = []
Cv = []
X = []

for l in L:
    file = "results/evolution_L=%s.txt" % (l)
    E.append(np.loadtxt(file, usecols=1))
    M.append(np.loadtxt(file, usecols=2))
    Cv.append(np.loadtxt(file, usecols=3))
    X.append(np.loadtxt(file, usecols=4))


maxX = np.argmax(X, axis=1)
fit = np.polyfit(1. / L, t[maxX], 1)
polynom = np.poly1d(fit)

fig = plt.figure()
plt.plot(1. / L, t[maxX], "o")
plt.plot(1. / L, polynom(1. / L))
plt.xlabel("1/L")
plt.ylabel("Tc")
plt.legend(["Finite Lattice", "%.4f x + %.4f" % (fit[0], fit[1])])
plt.grid()
fig.savefig("plots/critTemp.pdf")

fig = plt.figure()
for i in range(len(L)):
    plt.plot(t, E[i], linewidth=0.8)
plt.xlabel("T")
plt.ylabel("<E>")
plt.legend(["L=40", "L=60", "L=100", "L=160"])
plt.grid()
fig.savefig("plots/evolution_energy.pdf")

fig = plt.figure()
for i in range(len(L)):
    plt.plot(t, M[i], linewidth=0.8)
plt.xlabel("T")
plt.ylabel("<|M|>")
plt.legend(["L=40", "L=60", "L=100", "L=160"])
plt.grid()
fig.savefig("plots/evolution_magnetization.pdf")

fig = plt.figure()
for i in range(len(L)):
    plt.plot(t, Cv[i], linewidth=0.8)
plt.xlabel("T")
plt.ylabel("Cv")
plt.legend(["L=40", "L=60", "L=100", "L=160"])
plt.grid()
fig.savefig("plots/evolution_cv.pdf")

fig = plt.figure()
for i in range(len(L)):
    plt.plot(t, X[i], linewidth=0.8)
plt.xlabel("T")
plt.ylabel("$\chi$")
plt.legend(["L=40", "L=60", "L=100", "L=160"])
plt.grid()
fig.savefig("plots/evolution_susceptibility.pdf")
# -----------------------------------------------------------------------------
