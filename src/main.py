if __name__ == "__main__":
    from splitter import Splitter
    from bandits import EpsilonGreedyBandit, UCBBandit, ThompsonSamplingBandit
    from plot import plot_results_graph
    import matplotlib.pyplot as plt
    from numpy import arange
    from copy import deepcopy

    spl = Splitter("../data/ratings_binary.txt", " ")
    #for eps in [round(0.1*i, 2) for i in range(11)]:
    #    bandit = EpsilonGreedyBandit(deepcopy(spl), epsilon = eps, criteria = "cummulative_mean")
    #    bandit.output_to_file("../results/gridSearch/eps{0}_epoch_cm100_wmean.txt".format(eps),
    #                          "../results/gridSearch/eps{0}_recall_cm100_wmean.txt".format(eps))

    for alpha in [10**i for i in range(-2, 4)]:
        bandit = UCBBandit(deepcopy( spl ), param = alpha)
        bandit.output_to_file("../results/gridSearch/ucb{0}_epoch_cm100_mean.txt".format(alpha),
                              "../results/gridSearch/ucb{0}_recall_cm100_mean.txt".format(alpha))
    #fig = plt.figure()
    #for eps in [round(0.1*i, 2) for i in range(11)]:
    #        res_file = "../results/gridSearch/eps{0}_recall_cm100_wmean.txt".format(eps)
    #        plot_results_graph(res_file, "eps={}".format(eps))

    #plt.legend()
    #plt.savefig("../results/Recall.png")
    #plt.show()
    #spl = Splitter("../data/ratings_binary.txt", " ")
    #bandit = UCBBandit(spl, criteria="cummulative_mean")
    #bandit.output_to_file("../results/ucb2_epoch_cm100_wmean.txt",
    #                      "../results/ucb2_recall_cm100_wmean.txt")

    #spl = Splitter("../data/ratings_binary.txt", " ")
    #eps = 0.1
    #bandit = EpsilonGreedyBandit(spl, criteria="cummulative_mean")
    #bandit.output_to_file("../results/eps{0}_epoch_cm100_wmean.txt".format(eps),
    #                      "../results/eps{0}_recall_cm100_wmean.txt".format(eps))

    #spl = Splitter("../data/ratings_binary.txt", " ")
    #bandit = ThompsonSamplingBandit(spl, criteria="cummulative_mean")
    #bandit.output_to_file("../results/ts_epoch_cm100_wmean.txt",
    #                      "../results/ts_recall_cm100_wmean.txt")
