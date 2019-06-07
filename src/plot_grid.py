import numpy as np
import matplotlib.colors as cl
import scipy.ndimage
from plot import plot_results_graph
import seaborn as sns
import matplotlib.pyplot as plt

fontsize=12
alg = ["Eps",  "UCB"]
dataset = ["cm100k", "ML", "twitter"]
path = "../results/memoria/{0}/Recall{1}.png"

fig, ax = plt.subplots(2,3, sharex = True, sharey = True)
sns.set()
sns.set_context("paper")
sns.set_style("white")
for i in range(2):
    for j in range(3):
        filename = path.format(dataset[j], alg[i])
        print(filename)
        try:
            img = plt.imread(filename)
        except:
            pass
        ax[i][j].imshow(img[50:,:-50,:])
        ax[i][j].axis('off')

fig.tight_layout()
plt.show()
