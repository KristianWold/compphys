#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import numpy as np
import matplotlib.pyplot as plt
import math as m
import sys

# Set fontsizes in figures
params = {'legend.fontsize': 'x-large',
          'axes.labelsize': 'x-large',
          'axes.titlesize': 'x-large',
          'xtick.labelsize': 'x-large',
          'ytick.labelsize': 'x-large'}
plt.rcParams.update(params)

accepted = []
N = [1000, 2000, 3000, 4000, 5000, 6000]

for n in N:
    os.system("mpirun -np 8 ./simulation.x %s 0 20 2" % n)
    accepted.append(np.loadtxt("results/meta.txt", usecols=0)[5])

fig = plt.figure()
plt.plot(N, accepted, "o-")
plt.xlabel("Cycles")
plt.ylabel("Accepted States")
plt.legend(["Accepted states, L=20, T = 2"])
plt.grid()
fig.savefig("plots/acceptedCycles.pdf")

accepted = []
T = np.linspace(1, 3, 20)
for t in T:
    os.system("mpirun -np 8 ./simulation.x 10000 0 20 %s" % t)
    accepted.append(np.loadtxt("results/meta.txt", usecols=0)[5])

accepted = np.array(accepted)/10000

fig = plt.figure()
plt.plot(T, accepted, "o-")
plt.xlabel("T")
plt.ylabel("Accepted States Per Sweep")
plt.legend(["Accepted states, L=20, cycles = 10000"])
plt.grid()
fig.savefig("plots/acceptedTemp.pdf")
