import matplotlib.pyplot as plt

def plot(path):
    X = []
    Y = []
    with open(path, 'r') as f:
        for line in f:
            data = line.split("\t")
            X.append(int(data[0]))
            Y.append(float(data[1]))
    fig = plt.figure()
    plt.ylim((0,0.005))
    plt.plot(X,Y)
    plt.show()


plot("../data/results/precision.txt")
plot("../data/results/recall.txt")
