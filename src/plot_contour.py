import numpy as np
import matplotlib.colors as cl
import scipy.ndimage
from plot import plot_results_graph
import seaborn as sns
import matplotlib.pyplot as plt

fontsize=12
alg = ["eps",  "ucb", "thompson",]
alg_name = [r"$\epsilon$-Greedy", "UCB", "Thompson Sampling"]
dataset = ["cm100k", "movieLens", "twitter"]
dataset_name = ["CM100k", "MovieLens", "Twitter"]
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
        Z = np.array(Z)
        Z = Z.transpose()
        X = np.arange(1,11, 10/30)
        print(len(X), len(Z))
        ax[i][j].contour(X,X,Z, colors=["black"], linewidths=[0.8], levels=20)
        cont = ax[i][j].contourf(X,X,Z, cmap=plt.get_cmap("RdBu"), norm=cl.Normalize(vmin=vmin, vmax=vmax), levels=20)
        cb = plt.colorbar(cont, fraction=0.05, ax = ax[i][j])
        #cb.ax.tick_params(labelsize=fontsize)
        ax[i][j].set_xticks([])
        ax[i][j].set_yticks([])
        if i == 0:
            ax[i][j].set_title(dataset_name[j])
        if i == 2:
            ax[i][j].tick_params(axis='both', which='major', labelsize=fontsize)
            ax[i][j].set_xlabel(r"$\alpha$", fontsize=fontsize)
            ax[i][j].set_xticks(range(1,11))
        if j == 0:
            ax[i][j].tick_params(axis='both', which='minor', labelsize=fontsize)
            ax[i][j].set_ylabel(alg_name[i]+"\n"+r"$\beta$", fontsize=fontsize)
            ax[i][j].set_yticks(range(1,11))
        ax[i][j].set_xlim((1,10))
        ax[i][j].set_ylim((1,10))
plt.show()
