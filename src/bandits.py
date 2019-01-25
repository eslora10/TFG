# TODO: Considerar la opcion de tener train

import numpy as np
import matplotlib.pyplot as plt
import random
import seaborn as sns
from bisect import insort
from math import sqrt

class ItemBandit():
    """
    """
    def __init__(self, item, value = 0, count = 0, time = 0, reward = 0, uncertainty = 0):
        """
        """
        self.item = item
        self.value = value
        self.count = count
        self.time = time
        self.reward = reward
        self.uncertainty = uncertainty

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
        self.actions = self.init_items(splitter) # sorted([ItemBandit(item) for item in splitter.item_set])
        self.len_actions = len(self.actions)
        len_test_ini = splitter.test_len
        self.cummulative_recall = [0]
        recall = 0

        self.time = 1
        while splitter.test_set:
            for user in splitter.user_set:
                if user in splitter.test_set.keys():
                    item = self.select_item(splitter, user)
                    # Remove the item from the ordered actions set
                    item.count+=1
                    if item.item in splitter.test_set[user].keys():
                        current_value = item.value
                        n = item.count
                        reward = splitter.test_set[user][item.item]
                        self.update_item_info(item, current_value, n, reward, criteria)
                        # Remove the user from the item_user set
                        try:
                            splitter.item_users[item.item].remove(user)
                            if not splitter.item_users[item.item]:
                                item.time = self.time
                        except KeyError:
                            pass
                    else:
                        # In case we don't have info about the item we add it to the train
                        # set with reward=0
                        reward = 0
                    # Update recall
                    recall += reward
                    # Update train and test
                    self.update_train_test(splitter, user, item, reward)
                    # Reinsert the item in its new position
                    insort(self.actions, item)
                self.time += 1
            self.cummulative_recall.append(recall/len_test_ini)

    def update_train_test(self, splitter, user, item, reward):
        # Remove item from the test_set
        try:
            splitter.test_set[user].pop(item.item)
            if not splitter.test_set[user]:
                splitter.test_set.pop(user)
        except:
            pass
        # Insert the item in the train_set
        try:
            splitter.train_set[user][item.item] = reward
        except KeyError:
            splitter.train_set[user] = {item.item: reward}

    def init_items(self, splitter):
        return sorted([ItemBandit(item) for item in splitter.item_set])

    def select_item(self, splitter, user):
        pass

    def update_item_info(self, item, value, count, reward, criteria):
        pass

    def output_to_file(self, filepath, filepath_2):
        with open(filepath, 'w') as output:
            output.write("Total times: {0}\n".format(self.time))
            output.write("Item\tTime empty\tEstimated value\tTime\n")
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

    def update_item_info(self, item, value, count, reward, criteria):
        item.reward += reward
        if criteria == "mean":
            item.value = 1/count*((count-1)*value + reward)
        elif criteria == "cummulative_mean":
            item.value = 1/2*(value + reward)
        else:
            item.value = criteria(count, value, reward)

class UCBBandit(Bandit):

    def __init__(self, splitter, criteria="mean", param=2):
        self.param = param
        super().__init__(splitter, criteria=criteria)

    def init_items(self, splitter):
        tam_item = len(splitter.item_set)
        uncertainty = sqrt(tam_item) # After doing this initialation this would be the uncertainty
        actions = []
        items = list(splitter.item_set)
        users = list(splitter.user_set)
        tam_users = len(users)
        for i in range(tam_item):
            item = items[i]
            user = users[i%tam_users]
            if item in splitter.test_set[user].keys():
                reward = splitter.test_set[user][item]
            else:
                reward = 0

            itemb = ItemBandit(item, value = reward + uncertainty, count = 1, reward = reward, uncertainty = uncertainty)
            actions.append(itemb)
            self.update_train_test(splitter, user, itemb, reward)
        return sorted(actions)

    def update_item_info(self, item, value, count, reward, criteria):
        item.reward += reward
        item.uncertainty = self.param*sqrt(np.log(self.time)/item.count)
        item.value = item.reward + item.uncertainty # 1/count*((count-1)*value + reward) + uncertainty

        for item2 in self.actions:
            if item2.item != item.item:
                item2.uncertainty = self.param*sqrt(np.log(self.time)/item2.count)
                item2.value = item2.reward + item2.uncertainty
        self.actions = sorted(self.actions)

    def select_item(self, splitter, user):
        i = 0
        item = self.actions[i]
        while user in splitter.train_set.keys() and item.item in splitter.train_set[user]:
            i += 1
            item = self.actions[i]
        self.actions.pop(i)
        return item

if __name__=="__main__":
    from splitter import Splitter

    fig = plt.figure()
    # for eps in [10, 2, 0]:
    #     spl = Splitter("../data/ratings_binary.txt", " ")
    #     bandit = UCBBandit(spl, param=eps)
    #     bandit.output_to_file("../results/ucb{0}_epoch.txt".format(eps),
    #                             "../results/ucb{0}_recall.txt".format(eps))

    spl = Splitter("../data/ratings_binary.txt", " ")
    eps = 2
    bandit = UCBBandit(spl)
    bandit.output_to_file("../results/ucb{0}_epoch.txt".format(eps),
                          "../results/ucb{0}_recall.txt".format(eps))
