# TODO: Considerar la opcion de tener train

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
        self.len_actions = len(self.actions)
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
                        # self.actions.remove(item)
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
                        #insort(self.actions, item)
                    else:
                        # In case we don't have info about the item we add it to the train
                        # set with reward=0
                        reward = 0
                    try:
                        splitter.train_set[user][item.item] = reward
                    except KeyError:
                        splitter.train_set[user] = {item.item: reward}

                    # Reinsert the item in its new position
                    insort(self.actions, item)
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
            #item = random.sample(self.actions, 1)[0]
            i = np.random.randint(self.len_actions)
            item = self.actions[i]
            while user in splitter.train_set.keys() and item.item in splitter.train_set[user]:
                #item = random.sample(self.actions, 1)[0]
                i = np.random.randint(self.len_actions)
                item = self.actions[i]
        self.actions.pop(i)
        return item


if __name__=="__main__":
    from splitter import Splitter

    fig = plt.figure()
    for eps in [1, 0.5,0.1]:
        spl = Splitter("../data/ratings_binary.txt", " ")
        bandit = EpsilonGreedyBandit(eps, spl)
        bandit.output_to_file("../results/epsilon{0}_greedy_bandit.txt".format(eps),
                              "../results/bandit_recall{0}.txt".format(eps))
