import numpy as np
import matplotlib.pyplot as plt
import random
import seaborn as sns

class Bandit():
    """
    """

    def __init__(self, splitter, criteria="mean"):
        splitter = splitter
        self.actions = {item: {"count": 0, "value": 0} for item in splitter.item_set}
        self.max_item = random.sample(splitter.item_set, 1)[0]
        self.max_item_value = 0
        len_test_ini = splitter.test_len
        self.cummulative_recall = [0]
        recall = 0

        self.epoch = 0
        while splitter.test_set:
            for user in splitter.user_set:
                if user in splitter.test_set.keys():
                    while True:
                        item = self.select_item(splitter)
                        # Check if we have info about the item and if we haven't reccomended the item
                        # before to the same user
                        if (user not in splitter.train_set \
                            or item not in splitter.train_set[user])\
                            and item in splitter.test_set[user]:

                            self.actions[item]["count"] += 1
                            if splitter.test_set[user][item]:
                                current_value = self.actions[item]["value"]
                                n = self.actions[item]["count"]
                                reward = splitter.test_set[user][item]
                                # Update the item info
                                if criteria == "mean":
                                    self.actions[item]["value"] = 1/n*((n-1)*current_value + reward)
                                elif criteria == "cummulated_mean":
                                    self.actions[item]["value"] = 1/2*(current_value + reward)
                                else:
                                    self.actions[item]["value"] = criteria(n, current_value, reward)
                            if self.actions[item]["value"] > self.max_item_value:
                                self.max_item_value = self.actions[item]["value"]
                                self.max_item = item

                            # Remove item from the test_set and add it to the train_set
                            reward = splitter.test_set[user].pop(item)
                            recall += reward
                            if not splitter.test_set[user]:
                                splitter.test_set.pop(user)
                            try:
                                splitter.train_set[user][item] = reward
                            except KeyError:
                                splitter.train_set[user] = {item: reward}
                            self.epoch += 1
                            self.cummulative_recall.append(recall/len_test_ini)
                            break

    def select_item(self, splitter):
        pass

    def output_to_file(self, filepath, filepath_2):
        with open(filepath, 'w') as output:
            output.write("Total epochs: {0}\n".format(self.epoch))
            output.write("Item\tTimes selected\tEstimated value\n")
            for action, item in sorted(self.actions.items(), key=lambda item: item[1]["count"], reverse=True):
                output.write("{0}\t{1}\t{2}\n".format(action, item["count"], item["value"]))
        with open(filepath_2, 'w') as output:
            for i in range(len(self.cummulative_recall)):
                output.write("{0}\t{1}\n".format(i, self.cummulative_recall[i]))


class EpsilonGreedyBandit(Bandit):
    """
    """

    def __init__(self, epsilon, splitter, criteria="mean"):
        self.epsilon = epsilon
        super().__init__(splitter, criteria=criteria)

    def select_item(self, splitter):
        if np.random.binomial(1, 1-self.epsilon):
            # Exploitation
            item = self.max_item
        else:
            # Exploration
            item = random.sample(splitter.item_set, 1)[0]
        return item


def plot_results_hist(results_file, num_items = 0):
    with open(results_file, 'r') as infile:
        infile.readline() # Total epoch
        infile.readline() # Header
        X = []
        Y1 = []
        Y2= []
        if num_items:
            for _ in range(num_items):
                line = infile.readline().strip('\n').split('\t')
                X.append(int(line[0]))
                Y1.append(int(line[1]))
                Y2.append(float(line[2]))
        else:
            for line in infile:
                li = line.strip('\n').split('\t')
                X.append(int(li[0]))
                Y1.append(int(li[1]))
                Y2.append(float(li[2]))

        fig, (fig_1, fig_2) = plt.subplots(2, 1)
        fig_1.bar(range(len(X)), Y1, tick_label = X)
        fig_1.set_title("Number of times selected")
        fig_2.bar(range(len(X)), Y2, tick_label = X)
        fig_2.set_title("Estimated value")
        fig.savefig(results_file+'.png')
        plt.close(fig)

def plot_results_graph(results_file, eps):
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
    from splitter import Splitter

    fig = plt.figure()
    for eps in [1, 0.5,0.1]:
        spl = Splitter("../data/ratings_binary.txt", " ")
        bandit = EpsilonGreedyBandit(0.9, spl)
        bandit.output_to_file("../results/epsilon{0}_greedy_bandit.txt".format(eps), "../results/bandit_recall.txt")

        plot_results_hist("../results/epsilon{0}_greedy_bandit.txt".format(eps), 10)
        plot_results_graph("../results/bandit_recall.txt", eps)

    plt.legend()
    plt.savefig("EpsilonGreedy.png")
    plt.show()
