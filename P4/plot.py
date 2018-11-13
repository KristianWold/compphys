import numpy as np
import matplotlib.pyplot as plt

# Information about the dimmensions of the data set
meta = np.loadtxt("results/meta.txt", usecols=0)

cycles = int(meta[0])
cutoff = int(meta[1])
cores = int(meta[2])
L = int(meta[3])
T = float(meta[4])

# data set generated by the Monte Carlo simulation
array = np.fromfile("results/data.dat", dtype="int32", count=-1)

E = np.zeros((cores, cycles))
M = np.zeros((cores, cycles))

for i in range(cores):
    start = 2 * cycles * i
    end = 2 * cycles * i + cycles
    E[i] = array[start:end]
    M[i] = array[(start + cycles):(end + cycles)]


fig = plt.figure()
plt.plot(E[i] / L**2)
plt.xlabel("Cycle")
plt.ylabel("Energy per spin")
plt.legend(["energy, L=%s, T=%s" % (L, T)])
#    plt.legend("Energy of system")
fig.savefig("plots/plot_energy_L=%s_T=%s.pdf" % (L, T))

fig = plt.figure()
plt.plot(M[i] / L**2)
plt.xlabel("Cycle")
plt.ylabel("magnetization per spin")
plt.legend(["magnetization, L=%s, T=%s" % (L, T)])
#    plt.legend("Energy of system")
fig.savefig("plots/plot_magnetization_L=%s_T=%s.pdf" % (L, T))


# probability distribution
# -----------------------------------------------------------------------------
state = np.loadtxt("results/distribution.txt", usecols=0)
prob = np.loadtxt("results/distribution.txt", usecols=1)

fig = plt.figure()
plt.plot(state, prob, "o")
plt.xlabel("energy")
plt.ylabel("probability")
plt.legend(["distribution, L=%s, T=%s" % (L, T)])
fig.savefig("plots/distribution_L=%s_T=%s.pdf" % (L, T))
# -----------------------------------------------------------------------------

# numerical vs. analytical
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
