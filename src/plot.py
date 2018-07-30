import matplotlib.pyplot as plt
import numpy as np
import sys

def plot(path):
    X = []
    precision = [0]
    recall = [0]
    sum_hits = [0]
    coverage = []
    with open(path, 'r') as f:
        f.readline()
        for line in f:
            data = line.split("\t")
            X.append(int(data[0]))
            precision.append(precision[-1]+float(data[1]))
            recall.append(recall[-1]+float(data[2]))
            # hits.append(int(data[3]))
            sum_hits.append(sum_hits[-1]+int(data[3]))
            coverage.append(float(data[4]))
    fig, ( ax1, ax2 ) = plt.subplots(2,1)
    ax1.plot(X,precision[1:], label="Precision")
    ax1.plot(X,recall[1:], label="Recall")
    ax1.legend(loc=1)
    # ax2.plot(X,hits, label="Hits")
    ax2.plot(X, sum_hits[1:], label="Sum hits")
    ax2.legend(loc=1)
    plt.show()


plot(sys.argv[1])


