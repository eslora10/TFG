import numpy as np
import matplotlib.colors as cl
import scipy.ndimage
from plot import plot_results_graph
import seaborn as sns
import matplotlib.pyplot as plt

fontsize=12
fig = plt.figure()
sns.set()
sns.set_context("paper")
sns.set_style("white")
ax = fig.add_subplot(111)
colors = sns.hls_palette(4, l=.4, s=.8)
ax.tick_params(axis='both', which='major', labelsize=fontsize)
ax.tick_params(axis='both', which='minor', labelsize=fontsize)
ax.set_prop_cycle('color', colors)

filename = "../results/gridSearch/eps/movieLens/param/eps0.001_epoch_cm100_wmean.txt"
plot_results_graph(filename, "0.001-Greedy", "../results/gridSearch/random_movieLens.txt")

filename = "../results/gridSearch/ucb/movieLens/param/ucb0.1.txt"
plot_results_graph(filename, r"UCB $\gamma = 0.1$", "../results/gridSearch/random_movieLens.txt")

#filename = "../results/gridSearch/thompson/movieLens"
#plot_results_graph(filename, r"Thompson Sampling $\alpha = 1, \beta = 8$", "../results/gridSearch/random_movieLens.txt")

plt.legend(fontsize=fontsize)
plt.savefig("../results/memoria/movieLens/RecallComp.png")
plt.show()
plt.close()
