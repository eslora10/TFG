import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import scipy.ndimage

with open("../results/gridSearch/eps/cm100k/optimistic/eps_cut.txt", "r") as entrada:
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
    vmin = min(zvals)
    vmax = max(zvals)
    print(vmin, vmax)
    Z = scipy.ndimage.zoom(Z, 3)
    X = np.arange(1,11, 10/30)
    plt.contour(X,X,Z, colors=["black"], linewidths=[0.8])
    plt.contourf(X,X,Z, cmap=plt.get_cmap("bwr"), norm=colors.Normalize(vmin=vmin, vmax=vmax))
    plt.colorbar()
    plt.ylabel(r"$\alpha$")
    plt.xlabel(r"$\beta$")
    plt.xlim((1,10))
    plt.ylim((1,10))
    plt.show()
