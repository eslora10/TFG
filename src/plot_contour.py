import numpy as np
import matplotlib.colors as cl
import scipy.ndimage
from plot import plot_results_graph
import seaborn as sns
import matplotlib.pyplot as plt

fontsize=12
alg = ["eps",  "ucb", "thompson",]
dataset = ["cm100k", "movieLens", "twitter"]
path = "../results/gridSearch/{0}/{1}/optimistic/cut.txt"

fig, ax = plt.subplots(3,3)
sns.set()
sns.set_context("paper")
sns.set_style("white")
for i in range(3):
    for j in range(3):
        print(path.format(alg[i], dataset[j]))
        try:
            with open(path.format(alg[i], dataset[j]), "r") as entrada:
                Z = []
                k = 0
                sub = []
                zvals = []
                for line in entrada:
                    vals = line.strip("\n").split(",")
                    zvals.append(float(vals[2]))
                    if k == 10:
                        Z.append(sub)
                        sub = []
                        k = 0
                    sub.append(float(vals[2]))
                    k+=1
        except:
            continue
        Z.append(sub)
        vmin = min(zvals)
        vmax = max(zvals)
        Z = scipy.ndimage.zoom(Z, 3)
        X = np.arange(1,11, 10/30)
        print(len(X), len(Z))
        ax[i][j].tick_params(axis='both', which='major', labelsize=fontsize)
        ax[i][j].tick_params(axis='both', which='minor', labelsize=fontsize)
        ax[i][j].contour(X,X,Z, colors=["black"], linewidths=[0.8], levels=20)
        cont = ax[i][j].contourf(X,X,Z, cmap=plt.get_cmap("RdBu"), norm=cl.Normalize(vmin=vmin, vmax=vmax), levels=20)
        cb = plt.colorbar(cont, fraction=0.05, ax = ax[i][j])
        #cb.ax.tick_params(labelsize=fontsize)
        ax[i][j].set_ylabel(r"$\alpha$", fontsize=fontsize)
        ax[i][j].set_xlabel(r"$\beta$", fontsize=fontsize)
        ax[i][j].set_xlim((1,10))
        ax[i][j].set_ylim((1,10))
plt.show()
