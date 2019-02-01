import matplotlib.pyplot as plt
import seaborn as sns

def plot_results_scatter(results_file, eps, num_items = None):
    sns.set()
    sns.axes_style("darkgrid")
    sns.set_context("paper")
    with open(results_file, 'r') as infile:
        infile.readline() # Total epoch
        infile.readline() # Header
        X = []
        Y1 = []
        Y2= []
        lines = infile.readlines()[:num_items]
        for line in lines:
            spl = line.strip('\n').split('\t')
            X.append(int(spl[0]))
            Y1.append(int(spl[1]))
            Y2.append(float(spl[2]))


        plt.scatter(Y2, Y1, label=eps)
        plt.title("Epoch empty")
        plt.xlabel("Value")
        plt.ylabel("Epoch empty")

def plot_results_graph(results_file, eps):
    sns.set()
    sns.axes_style("darkgrid")
    sns.set_context("paper")
    with open(results_file) as infile:
        X = []
        Y = []
        for line in infile:
            li = line.strip('\n').split('\t')
            X.append(int(li[0]))
            Y.append(float(li[1]))

        plt.plot(X, Y, label=eps)
        plt.xlabel("Epoch")
        plt.ylabel("Cummulative recall")

if __name__=="__main__":
    fig = plt.figure()
    files = ["ts", "eps0.1", "ucb2"]#, "random"]
    for crit in ["mean"]: #, "wmean"]:
        for f in files:
            res_file = "../results/cm100/" + f + "_recall_cm100_"+ crit + ".txt"
            plot_results_graph(res_file, f + crit)

    plot_results_graph("../results/cm100/random_recall.txt", "random")
    plot_results_graph("../results/popularity_recall_cm100.txt", "popularity")
    plt.legend()
    plt.savefig("../results/Recall.png")
    plt.show()


    fig = plt.figure()

    for crit in ["mean", "wmean"]:
        for f in files:
            res_file = "../results/cm100/" + f + "_epoch_cm100_" + crit + ".txt"
            plot_results_scatter(res_file, f + crit)

    plt.legend()
    plt.savefig("../results/Epoch.png")
    #plt.show()
