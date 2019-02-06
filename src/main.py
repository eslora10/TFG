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
    action = sys.argv[2]
    EPS = 0.1
    UCB = 2

    spl = Splitter("../data/ratings_binary.txt", " ")
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
#            colors = sns.color_palette("hls", len(values))
#            ax.set_prop_cycle('color', colors)
#            for eps in values:
#                res_file = "../results/gridSearch/eps/eps{0}_recall_cm100_wmean.txt".format(eps)
#                plot_results_graph(res_file, "eps={}".format(eps))


#    plt.legend()
#    plt.savefig("../results/gridSearch/Recall"+ alg +".png")
#    plt.show()

    if action == "param":
        if alg == "Epsilon":
            values = [0, 0.001, 0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
            for eps in values:
                bandit = EpsilonGreedyBandit(deepcopy(spl), epsilon = eps, criteria = "cummulative_mean")
                bandit.output_to_file("../results/gridSearch/eps/eps{0}_epoch_cm100_wmean.txt".format(eps),
                                      "../results/gridSearch/eps/eps{0}_recall_cm100_wmean.txt".format(eps))

        elif alg == "UCB":
            values == [0.01, 0.1, 1, 2, 10, 100]
            for param in values:
                bandit = UCBBandit(deepcopy( spl ), param = param)
                bandit.output_to_file("../results/gridSearch/ucb/ucb{0}_epoch_cm100_wmean.txt".format(param),
                                      "../results/gridSearch/ucb/ucb{0}_recall_cm100_wmean.txt".format(param))

        elif alg == "Thompson":
            print("No param in Thompson")

    elif action == "optimistic":
        alpha = 1
        values = range(1, 11)
        for beta in values:
            if alg == "Epsilon":
                bandit = EpsilonGreedyBandit(deepcopy(spl), epsilon = EPS, alpha = alpha, beta = beta, criteria = "cummulative_mean")
                path = "../results/gridSearch/eps/eps"
            elif alg == "UCB":
                bandit = UCBBandit(deepcopy(spl), param = UCB, alpha = alpha, beta = beta)
                path = "../results/gridSearch/ucb/ucb"
            elif alg == "Thompson":
                bandit = ThompsonSamplingBandit(deepcopy(spl), alpha = alpha, beta = beta)
                path = "../results/gridSearch/thompson/thompson"
            bandit.output_to_file(path + "{0}_{1}_epoch_cm100.txt".format(alpha, beta),
                                  path + "{0}_{1}_recall_cm100.txt".format(alpha, beta))
        beta = 1
        values = range(2, 11)
        for alpha in values:
            if alg == "Epsilon":
                bandit = EpsilonGreedyBandit(deepcopy(spl), epsilon = EPS, alpha = alpha, beta = beta, criteria = "cummulative_mean")
            elif alg == "UCB":
                bandit = UCBBandit(deepcopy(spl), param = UCB, alpha = alpha, beta = beta)
            elif alg == "Thompson":
                bandit = ThompsonSamplingBandit(deepcopy(spl), alpha = alpha, beta = beta)

