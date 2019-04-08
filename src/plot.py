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
        i = 0
        for line in infile:
            if i == 4950:
                break
            X.append(i)
            try:
                li = line.strip('\n')#.split('\t')
                #X.append(int(li[0]))
                Y.append(float(li))
            except ValueError:
                li = li.split("\t")
                Y.append(float(li[1]))
            i+=1

        plt.plot(X, Y, label=eps, linewidth = 1)
        plt.xlabel("Época", fontsize=12)
        plt.ylabel("Recall acumulado", fontsize=12)

if __name__=="__main__":
    """
    fig = plt.figure()
    files = ["eps999", "ucb999", "ts999", "random"]#, "random"]
    for crit in ["mean"]: #, "wmean"]:
        for f in files:
            res_file = "../results/" + f + "_recall_cm100.txt"
            plot_results_graph(res_file, f + crit)

    #plot_results_graph("../results/cm100/random_recall.txt", "random")
    #plot_results_graph("../results/popularity_recall_cm100.txt", "popularity")
    plt.legend()
    plt.savefig("../results/Recall.png")
    plt.show()


    fig = plt.figure()

    for crit in ["mean", "wmean"]:
        for f in files:
            res_file = "../results/" + f + "_epoch_cm100.txt"
            plot_results_scatter(res_file, f + crit)

    plt.legend()
    plt.savefig("../results/Epoch.png")
    #plt.show()

    """
    X = []
    y = []
    #plt.rc('text', usetex=True)
    sns.set()
    sns.set_context("paper")
    with open("../results/gridSearch/eps/MovieLens/eps_movieLens_cut.txt", "r") as f:
        for line in f:
            parsed = line.strip("\n").split(",")
            X.append(float(parsed[0]))
            y.append(float(parsed[1]))

    plt.scatter(X, y, color="magenta")
    plt.plot(X, y, color="magenta")

    plt.xlabel('epsilon')
    plt.ylabel('recall=500')
    plt.show()

