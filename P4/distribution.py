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

T = [1, 2.4]

for t in T:
    os.system("mpirun -np 1 ./simulation.x 100000 1000 20 %s 1"%t)

    # Information about the dimmensions of the data set
    meta = np.loadtxt("results/meta.txt", usecols=0)
    Cv = np.loadtxt("results/expectation.txt", usecols=0)[3]

    # data set generated by the Monte Carlo simulation
    array = np.fromfile("results/data.dat", dtype="int32", count=-1)

    cycles = int(meta[0])
    cutoff = int(meta[1])
    cores = int(meta[2])
    L = float(meta[3])
    var = t**2*L**2*Cv
    print("Variance for T=%s is %s"%(t,var))

    length = cycles - cutoff

    E = array[cutoff:cycles]

    P = {}
    # Goes though the different enegy states that occured and counts how often they
    # occured.

    for i in range(length):
        energy = E[i]
        if energy in P:
            P[energy] += 1
        else:
            P[energy] = 1

    # Normalizes the probability
    for p in P:
        P[p] /= float(length)

    state = list(P.keys())      # state of a specific energy
    prob = list(P.values())     # probaility of energy to occur

    fig = plt.figure()
    plt.plot(state, prob, "o", markersize=4)
    plt.xlabel("$E_{tot} $ $[\,J\,]$")
    plt.ylabel("$P(E_{tot})$")
    plt.legend(["20x20 Lattice\nT=%s$[\,J/k_B\,]$" %t])
    plt.grid()
    plt.gcf().set_tight_layout(True)
    fig.savefig("plots/distribution_T=%s.pdf" %t)
