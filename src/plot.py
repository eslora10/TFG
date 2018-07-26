import matplotlib.pyplot as plt
import numpy as np

def plot(path):
    X = []
    precision = []
    recall = []
    hits = []
    coverage = []
    with open(path, 'r') as f:
        f.readline()
        for line in f:
            data = line.split("\t")
            X.append(int(data[0]))
            precision.append(float(data[1]))
            recall.append(float(data[2]))
            hits.append(float(data[3]))
            coverage.append(float(data[4]))
    fig, ( ax1, ax2 ) = plt.subplots(2,1)
    ax1.plot(X,precision, label="Precision")
    ax1.plot(X,recall, label="Recall")
    ax1.legend(loc=1)
    ax2.plot(X,hits, label="Hits")
    ax2.plot(X[:-1],np.diff(hits), label="Hits diff")
    ax2.legend(loc=1)
    plt.show()


plot("../results/07-25-18_random.txt")
