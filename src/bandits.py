# TODO: Optimizar la entrada y salida de los items de la lista de acciones
import numpy as np
import matplotlib.pyplot as plt
import random
import seaborn as sns
from bisect import insort

class ItemBandit():
    """
    """
    def __init__(self, item, value = 0, count = 0, time = 0):
        """
        """
        self.item = item
        self.value = value
        self.count = count
        self.time = time

    def __lt__(self, other):
        return self.value > other.value

    def __le__(self, other):
        return self.value >= other.value

    def __eq__(self, other):
        return self.item == other.item

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value < other.value

    def __ge__(self, other):
        return self.value <= other.value

    def __repr__(self):
        return '{0}\t{1}\t{2}\t{3}\n'.format(self.item, self.time, self.value, self.count)

class Bandit():
    """
    """

    def __init__(self, splitter, criteria="mean"):
        splitter = splitter
        self.actions = sorted([ItemBandit(item) for item in splitter.item_set])
        len_test_ini = splitter.test_len
        self.cummulative_recall = [0]
        recall = 0

        self.epoch = 0
        while splitter.test_set:
            for user in splitter.user_set:
                if user in splitter.test_set.keys():
                    item = self.select_item(splitter, user)
                    # Remove the item from the ordered actions set
                    item.count+=1
                    if item.item in splitter.test_set[user].keys():
                        self.actions.remove(item)
                        current_value = item.value
                        n = item.count
                        reward = splitter.test_set[user][item.item]
                        # Update the item info
                        if criteria == "mean":
                            item.value = 1/n*((n-1)*current_value + reward)
                        elif criteria == "cummulative_mean":
                            item.value = 1/2*(current_value + reward)
                        else:
                            item.value = criteria(n, current_value, reward)
                        # Remove the user from the item_user set
                        try:
                            splitter.item_users[item.item].remove(user)
                            if not splitter.item_users[item.item]:
                                item.time = self.epoch
                        except KeyError:
                            pass

                        # Remove item from the test_set
                        splitter.test_set[user].pop(item.item)
                        recall += reward
                        if not splitter.test_set[user]:
                            splitter.test_set.pop(user)
                        # Reinsert the item in its new position
                        insort(self.actions, item)
                    else:
                        # In case we don't have info about the item we add it to the train set with reward=0
                        reward = 0
                    try:
                        splitter.train_set[user][item.item] = reward
                    except KeyError:
                        splitter.train_set[user] = {item.item: reward}
            self.epoch += 1
            self.cummulative_recall.append(recall/len_test_ini)

    def select_item(self, splitter, user):
        pass

    def output_to_file(self, filepath, filepath_2):
        with open(filepath, 'w') as output:
            output.write("Total epochs: {0}\n".format(self.epoch))
            output.write("Item\tEpoch empty\tEstimated value\tTime\n")
            for item in self.actions:
                output.write(item.__repr__())
        with open(filepath_2, 'w') as output:
            for i in range(len(self.cummulative_recall)):
                output.write("{0}\t{1}\n".format(i, self.cummulative_recall[i]))


class EpsilonGreedyBandit(Bandit):
    """
    """

    def __init__(self, epsilon, splitter, criteria="mean"):
        self.epsilon = epsilon
        super().__init__(splitter, criteria=criteria)

    def select_item(self, splitter, user):
        # Check if we have info about the item and if we haven't reccomended the item
        # before to the same user

        if np.random.binomial(1, 1-self.epsilon):
            # Exploitation
            i = 0
            item = self.actions[i]
            while user in splitter.train_set.keys() and item.item in splitter.train_set[user]:
                i+=1
                item = self.actions[i]
        else:
            # Exploration
            item = random.sample(self.actions, 1)[0]
            while user in splitter.train_set.keys() and item.item in splitter.train_set[user]:
                item = random.sample(self.actions, 1)[0]
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
        fig_1.bar(range(len(X)), Y1)
        fig_1.set_title("Epoch empty")
        fig_2.bar(range(len(X)), Y2)
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
        bandit = EpsilonGreedyBandit(eps, spl)
        bandit.output_to_file("../results/epsilon{0}_greedy_bandit.txt".format(eps), "../results/bandit_recall.txt")

        plot_results_hist("../results/epsilon{0}_greedy_bandit.txt".format(eps))
        plot_results_graph("../results/bandit_recall.txt", eps)

    plt.legend()
    plt.savefig("EpsilonGreedy.png")
    plt.show()
