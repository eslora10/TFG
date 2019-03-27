import numpy as np
import matplotlib.colors as cl
import scipy.ndimage
from plot import plot_results_graph
import seaborn as sns
import matplotlib.pyplot as plt

nameparam = r"$\gamma$"
#nameparam = r"$\varepsilon$"
fontsize=12
path = "../results/gridSearch/ucb/cm100k/param/ucb{0}_recall_cm100_miniwmean.txt"
#path = "../results/gridSearch/eps/cm100k/param/eps{0}_recall_cm100_wmean.txt"
alg = "UCB"
#values = [0.0, 0.1, 0.2, 0.4, 0.6, 0.8, 1]
values = [0.01, 0.1, 1, 2, 10, 100]
fig = plt.figure()
sns.set()
sns.set_context("paper")
sns.set_style("white")
ax = fig.add_subplot(111)
colors = sns.hls_palette(len(values)+1, l=.4, s=.8)
ax.tick_params(axis='both', which='major', labelsize=fontsize)
ax.tick_params(axis='both', which='minor', labelsize=fontsize)
ax.set_prop_cycle('color', colors)
for value in values:
    filename = path.format(value)
    if value == 0.01:
        value = 0
    plot_results_graph(filename, nameparam+"={0}".format(value))

plot_results_graph("../results/gridSearch/random_cm100k.txt", "random")
plt.legend(fontsize=fontsize)
plt.savefig("../results/memoria/cm100k/Recall"+ alg +".png")
plt.show()
plt.close()


fig = plt.figure()
sns.set()
sns.set_context("paper")
sns.set_style("white")
ax = fig.add_subplot(111)
colors = sns.hls_palette(len(values)+1, l=.4, s=.8)
ax.tick_params(axis='both', which='major', labelsize=fontsize)
ax.tick_params(axis='both', which='minor', labelsize=fontsize)
ax.set_prop_cycle('color', colors)
X = []
Y = []
path = "../results/gridSearch/ucb/cm100k/param/ucb_cut.txt"
#path = "../results/gridSearch/eps/cm100k/param/eps_param.txt"
with open(path) as input_file:
    for line in input_file:
        spl = line.strip("\n").split(",")
        x = float(spl[0])
        y = float(spl[1])
        X.append(x)
        Y.append(y)
        plt.scatter([x], [y], s=50)
plt.plot(X, Y, color="black", linewidth = 1, zorder = -1)
plt.xlabel(nameparam, fontsize=fontsize)
plt.ylabel("Recall mitad", fontsize=fontsize)
plt.savefig("../results/memoria/cm100k/RecallMitad"+ alg +".png")
plt.show()
#path = "../results/gridSearch/thompson/cm100k/ts_cut.txt"
path = "../results/gridSearch/ucb/cm100k/optimistic/ucb_cut.txt"
#path = "../results/gridSearch/eps/cm100k/optimistic/eps_cut.txt"
with open(path, "r") as entrada:
    Z = []
    i = 0
    sub = []
    zvals = []
    for line in entrada:
        vals = line.strip("\n").split(",")
        zvals.append(float(vals[2]))
        if i == 10:
            Z.append(sub)
            sub = []
            i = 0
        sub.append(float(vals[2]))
        i+=1
Z.append(sub)
sns.set()
sns.set_context("paper")
sns.set_style("white")
vmin = min(zvals)
vmax = max(zvals)
Z = scipy.ndimage.zoom(Z, 3)
X = np.arange(1,11, 10/30)
fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.tick_params(axis='both', which='major', labelsize=fontsize)
ax.tick_params(axis='both', which='minor', labelsize=fontsize)
plt.contour(X,X,Z, colors=["black"], linewidths=[0.8], levels=20)
plt.contourf(X,X,Z, cmap=plt.get_cmap("RdBu"), norm=cl.Normalize(vmin=vmin, vmax=vmax), levels=20)
cb = plt.colorbar(fraction=0.05)
cb.ax.tick_params(labelsize=fontsize)
plt.ylabel(r"$\alpha$", fontsize=fontsize)
plt.xlabel(r"$\beta$", fontsize=fontsize)
plt.xlim((1,10))
plt.ylim((1,10))
plt.savefig("../results/memoria/cm100k/Mapa"+ alg +".png")
plt.show()
