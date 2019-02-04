if __name__ == "__main__":
    from splitter import Splitter
    from bandits import EpsilonGreedyBandit, UCBBandit, ThompsonSamplingBandit
    from plot import plot_results_graph
    import matplotlib.pyplot as plt
    from numpy import arange
    from copy import deepcopy
    import sys
    import seaborn as sns

    alg = sys.argv[1]

    spl = Splitter("../data/ratings_binary.txt", " ")
    fig = plt.figure()
    ax = fig.add_subplot(111)
    if alg == "Epsilon":
        values = [10**(-i) for i in range(1,6)]
        for eps in values:
            bandit = EpsilonGreedyBandit(deepcopy(spl), epsilon = eps, criteria = "cummulative_mean")
            bandit.output_to_file("../results/gridSearch/eps/eps{0}_epoch_cm100_wmean.txt".format(eps),
                                    "../results/gridSearch/eps/eps{0}_recall_cm100_wmean.txt".format(eps))
        colors = sns.color_palette("hls", len(values))
        ax.set_prop_cycle('color', colors)
        for eps in values:
            res_file = "../results/gridSearch/eps/eps{0}_recall_cm100_wmean.txt".format(eps)
            plot_results_graph(res_file, "eps={}".format(eps))

    elif alg == "UCB":
        values = [10**i for i in range(-2, 4)]
        for param in values:
            bandit = UCBBandit(deepcopy( spl ), param = param)
            bandit.output_to_file("../results/gridSearch/ucb/ucb{0}_epoch_cm100_mean.txt".format(param),
                                "../results/gridSearch/ucb/ucb{0}_recall_cm100_mean.txt".format(param))
        colors = sns.color_palette("hls", len(values))
        ax.set_prop_cycle('color', colors)
        for param in values:
            res_file = "../results/gridSearch/ucb/ucb{0}_recall_cm100_wmean.txt".format(param)
            plot_results_graph(res_file, "param={}".format(param))

    elif alg == "Thompson":
        values = range(1, 10)
        alpha = 1
        for beta in values:
            bandit = ThompsonSamplingBandit(deepcopy( spl ), alpha = alpha, beta = beta)
            bandit.output_to_file("../results/gridSearch/thompson/thompson{0}_{1}_epoch_cm100_mean.txt".format(alpha, beta),
                                  "../results/gridSearch/thompson/thompson{0}_{1}_recall_cm100_mean.txt".format(alpha, beta))

        values = range(2, 10)
        beta = 1
        for alpha in values:
            bandit = ThompsonSamplingBandit(deepcopy( spl ), alpha = alpha, beta = beta)
            bandit.output_to_file("../results/gridSearch/thompson/thompson{0}_{1}_epoch_cm100_mean.txt".format(alpha, beta),
                                  "../results/gridSearch/thompson/thompson{0}_{1}_recall_cm100_mean.txt".format(alpha, beta))

        colors = sns.color_palette("hls", len(values))
        ax.set_prop_cycle('color', colors)
        for alpha in range(1, 10):
            for beta in range(1, 10):
                res_file = "../results/gridSearch/thompson/thompson{0}_{1}_recall_cm100_wmean.txt".format(alpha, beta)
                plot_results_graph(res_file, "alpha={0}, beta={1}".format(alpha, beta))


    else:
        print("Error, param must be in [Epsilon, UCB, Thompson]")
        sys.exit()

    plt.legend()
    plt.savefig("../results/gridSearch/Recall"+ alg +".png")
    plt.show()
