import matplotlib.pyplot as plt
import numpy as np

def plot(path, fig, prec, rec):
    X = []
    precision = [0]
    recall = [0]
    sum_hits = [0]
    coverage = []
    with open("../results/07-30-18_"+path+".txt", 'r') as f:
        f.readline()
        for line in f:
            data = line.split("\t")
            X.append(int(data[0]))
            precision.append(precision[-1]+float(data[1]))
            recall.append(recall[-1]+float(data[2]))
            # hits.append(int(data[3]))
            sum_hits.append(sum_hits[-1]+int(data[3]))
            coverage.append(float(data[4]))
    prec.plot(X,precision[1:], label=path)
    prec.legend(loc=1)
    prec.set_ylabel("Cumulated precision")
    prec.set_xlabel("t")
    # rec.plot(X,hits, label="Hits")
    rec.plot(X,recall[1:], label=path)
    rec.set_ylabel("Cumulated recall")
    rec.set_xlabel("t")
    rec.legend(loc=1)

fig, ( prec, rec ) = plt.subplots(2,1)
for f in ["random","popularity"]:
    plot(f, fig, prec, rec)
plt.show()


