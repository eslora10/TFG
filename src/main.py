if __name__ == "__main__":
    from splitter import Splitter
    from bandits import EpsilonGreedyBandit, UCBBandit, ThompsonSamplingBandit
    from plot import plot_results_graph
    import matplotlib.pyplot as plt
    from numpy import arange
    from copy import deepcopy
    import sys
    import os
    import re
    import seaborn as sns

    alg = sys.argv[1]
    action = sys.argv[2]
    EPS = 0.1
    UCB = 2

    spl = Splitter("../data/ratings.txt", " ")

    if action == "param":
        if alg == "Epsilon":
            values = [0, 0.001, 0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
            for eps in values:
                bandit = EpsilonGreedyBandit(deepcopy(spl), epsilon = eps, criteria = "cummulative_mean")
                bandit.output_to_file("../results/gridSearch/eps/MovieLens/eps{0}_epoch_cm100_wmean.txt".format(eps),
                                      "../results/gridSearch/eps/MovieLens/eps{0}_recall_cm100_wmean.txt".format(eps))

        elif alg == "UCB":
            values = [0.01, 0.1, 1, 2, 10, 100]
            for param in values:
                bandit = UCBBandit(deepcopy( spl ),"../results/gridSearch/ucb/MovieLens/ucb{0}_recall_cm100_wmean.txt".format(param),  param = param)
                #bandit.output_to_file("../results/gridSearch/ucb/cm100k/ucb{0}_epoch_cm100_wmean.txt".format(param),
                #                      "../results/gridSearch/ucb/MovieLens/ucb{0}_recall_cm100_wmean.txt".format(param))

        elif alg == "Thompson":
            print("No param in Thompson")

    elif action == "optimistic":
        alpha = 1
        values = range(1, 11)
        for beta in values:
#            if alg == "Epsilon":
#                bandit = EpsilonGreedyBandit(deepcopy(spl), epsilon = EPS, alpha = alpha, beta = beta, criter#ia = "cummulative_mean")
#                path = "../results/gridSearch/eps/eps"
#            elif alg == "UCB":
#                bandit = UCBBandit(deepcopy(spl), param = UCB, alpha = alpha, beta = beta)
#                path = "../results/gridSearch/ucb/ucb"
#            elif alg == "Thompson":
            if alg == "Thompson":
                bandit = ThompsonSamplingBandit(deepcopy(spl), alpha = alpha, beta = beta, count_no_rating = False)
                path = "../results/gridSearch/thompson/thompson"
            bandit.output_to_file(path + "{0}_{1}_epoch_cm100.txt".format(alpha, beta),
                                  path + "{0}_{1}_recall_cm100.txt".format(alpha, beta))
        beta = 1
        values = range(2, 11)
        for alpha in values:
#            if alg == "Epsilon":
#                bandit = EpsilonGreedyBandit(deepcopy(spl), epsilon = EPS, alpha = alpha, beta = beta, criter#ia = "cummulative_mean")
#            elif alg == "UCB":
#                bandit = UCBBandit(deepcopy(spl), param = UCB, alpha = alpha, beta = beta)
#            elif alg == "Thompson":
            if alg == "Thomspon":
                bandit = ThompsonSamplingBandit(deepcopy(spl), alpha = alpha, beta = beta, count_no_rating = False)

            bandit.output_to_file(path + "{0}_{1}_epoch_cm100.txt".format(alpha, beta),
                                  path + "{0}_{1}_recall_cm100.txt".format(alpha, beta))

    elif action == "plot":
        path = "../results/gridSearch/"
        if alg == "Epsilon":
            path += "eps/"
        elif alg == "Thompson":
            path += "thompson/"
        elif alg == "UCB":
            path += "ucb/"

        path += "cm100k/"+sys.argv[3]+"/"

        files = os.listdir(path)
        fig = plt.figure()
        sns.set()
        sns.set_context("paper")
        ax = fig.add_subplot(111)
        colors = sns.color_palette("hls", len(files))
        if sys.argv[3] == "optimistic":
            ax.set_prop_cycle('color', colors)
            exp = re.compile("[a-z]*(\w+?)_(\w+?)_")
            for f in sorted( files ):
                print(f)
                gr = exp.match(f)
                alpha = gr[1]
                beta = gr[2]
                plot_results_graph(path+f, "alpha={0}, beta={1}".format(alpha, beta))
        else:
            ax.set_prop_cycle('color', colors)
            exp = re.compile("[a-z]*([0-9]\.*[0-9]*)")
            for f in sorted( files ):
                try:
                    print(f)
                    gr = exp.match(f)
                    param = gr[1]
                    print(param)
                    plot_results_graph(path+f, "{0}".format(param))
                except:
                    pass



        plt.legend()
        plt.savefig("../results/gridSearch/Recall"+ alg +".png")
        plt.show()
