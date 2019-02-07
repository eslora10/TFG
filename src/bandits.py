# -*- coding: utf-8 -*-
""" Module: bandits

This module implements several multi-armed-bandit algorithms applied to Recommender Systems

Todo:
    * Considerar la opcion de tener train
    * En ThompsonSampling no contar la ausencia de rating como fallo
    * Mirar la repeticion de codigo
    * En ThompsonSampling cambiar la implementación a fallo (IDEA: posiblemente contar la ausencia de valor como -1)
"""

import numpy as np
import matplotlib.pyplot as plt
import random
import seaborn as sns
from bisect import insort
from math import sqrt

class ItemBandit():
    """ Basic item to be reccomended with its parameters and atributes.

    Attributes:
        item (int): item id
        value (float): estimated value of an item, depends on the chosen algorithm
        count (int): numer of times each item has been chosen
        time (int): iteration were the item test became empty
        reward (float): ratio between successful recomendation and the number of times chosen
        uncertainty (float): how sure we are the item value is correct
        successes (int): number of successful recomendations
    """
    def __init__(self, item, value = 0, count = 0, time = 0, reward = 0, uncertainty = 0, successes = 0, failures = 0):
        self.item = item
        self.value = value
        self.time = time
        if successes + failures != 0:
            self.reward = successes/(successes + failures)
            self.count = successes + failures
        else:
            self.reward = reward
            self.count = count
        self.uncertainty = uncertainty
        self.successes = successes
        self.failures = failures

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
        return '{0}\t{1}\t{2}\t{3}\n'.format(self.item, self.time, self.reward, self.count)

class Bandit():
    """ Auxiliar abstract class to implement different bandits algorithms.

    Attributes:
        actions (:obj: `list` of :obj: `Item`): sorted list which contains all of the items to be recommended
        len_actions (int): length of the previous list
        cummulative_recall (list): list wich contains the evolution of the iteration
        time (int): number of iterations

    """

    def __init__(self, splitter, alpha = 0, beta = 0, criteria="mean", count_no_rating = True):
        """ Creates a new Bandit and perfoms the algorithm.

        Note:
            This is an abstract class and it should not be instanciated

        Args:
            splitter (:obj: `Splitter`): Object which contains both train and test
            criteria (str or callable, optional): how to compute the reward of an item
            alpha (int): number of successes supposed at the begining of the experiment
            beta (int): number of failures supposed at the begining of the experiment

        Returns:
            A Bandit object with the iteration finished.

        """
        self.len_actions = len(splitter.item_set)
        self.time = (alpha + beta)*self.len_actions
        self.actions = self.init_items(splitter, alpha, beta)
        self.count_no_rating = count_no_rating
        len_test_ini = splitter.test_len
        self.cummulative_recall = [0]
        recall = 0

        while splitter.test_set:
            for user in splitter.user_set:
                if user in splitter.test_set.keys():
                    item = self.select_item(splitter, user)
                    # Remove the item from the ordered actions set
                    if item.item in splitter.test_set[user].keys():
                        item.count+=1
                        n = item.count
                        reward = splitter.test_set[user][item.item]
                        self.update_item_info(item, n, reward, criteria)
                        # Remove the user from the item_user set
                        try:
                            splitter.item_users[item.item].pop(user)
                            if not splitter.item_users[item.item]:
                                item.time = self.time
                        except KeyError:
                            pass
                    else:
                        # In case we don't have info about the item we add it to the train
                        # set with reward=0
                        reward = 0
                        if self.count_no_rating:
                            item.count += 1
                            n = item.count
                            self.update_item_info(item, n, reward, criteria)
                    # Update recall
                    recall += reward
                    # Update train and test
                    self.update_train_test(splitter, user, item, reward)
                    # Reinsert the item in its new position
                    insort(self.actions, item)
                self.time += 1
            self.cummulative_recall.append(recall/len_test_ini)

    def update_train_test(self, splitter, user, item, reward):
        """ Given a user and an item, this function removes the item from the user test set and adds
        it to the user test set.

        Args:
            splitter (:obj: `Splitter`): Object which contains both train and test
            user (int): user id
            item (:obj: `ItemBandit`): item to change from test to train
            reward (int): 0 if the user didn't like the item or if there is no info in the test set, 1 otherwise

        Returns:
            None

        """
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

    def init_items(self, splitter, successes, failures):
        """ Creates the ItemBandit list to use during the algorithm.

        Args:
            splitter (:obj: `Splitter`): Object which contains both train and test

        Returns:
            A sorted list which contains the ItemBanit objects.

        """
        return sorted([ItemBandit(item, successes = successes, failures = failures) for item in splitter.item_set])

    def select_item(self, splitter, user):
        """ Selects and item from the action list following the each bandit specific strategy.

        Note:
            Removes the selected item from the action list

        Args:
            splitter (:obj: `Splitter`): Object which contains both train and test
            user (int): user to receive the item (needed to avoid reccomending the same item more than once)

        Returns:
            The ItemBanit chosen

        """
        pass

    def update_item_info(self, item, count, reward, criteria):
        """ Updates the item information each time an item has been chosen

        Args:
        item (:obj: `ItemBandit`):

        Returns:
            None

        """
        if criteria == "mean":
            item.reward = 1/count*((count-1)*item.reward + reward)
        elif criteria == "cummulative_mean":
            item.reward = 1/2*(item.reward + reward)
        else:
            item.reward = criteria(count, item.reward, reward)

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

    def __init__(self, splitter, epsilon=0.1, alpha = 0, beta = 0, criteria="mean", count_no_rating = True):
        self.epsilon = epsilon
        super().__init__(splitter, criteria=criteria, alpha = alpha, beta = beta, count_no_rating = count_no_rating)

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

    def update_item_info(self, item, count, reward, criteria):
        super().update_item_info(item, count, reward, criteria)
        item.value = item.reward

class UCBBandit(Bandit):

    def __init__(self, splitter, alpha = 0, beta = 0, criteria="mean", count_no_rating = True, param=2):
        self.param = param
        super().__init__(splitter, criteria=criteria, count_no_rating = count_no_rating, alpha = alpha, beta = beta)

    def init_items(self, splitter, successes, failures):
        tam_item = self.len_actions
        if successes + failures == 0:
            uncertainty = sqrt(self.param*tam_item) # After doing this initialation this would be the uncertainty
            actions = []
            items = list(splitter.item_set)
            users = list(splitter.user_set)
            tam_users = len(users)
            for i in range(tam_item):
                self.time += 1
                item = items[i]
                user = users[i%tam_users]
                if item in splitter.test_set[user].keys():
                    reward = splitter.test_set[user][item]
                else:
                    reward = 0

                itemb = ItemBandit(item, value = reward + uncertainty, count = 1, reward = reward, uncertainty = uncertainty)
                actions.append(itemb)
                self.update_train_test(splitter, user, itemb, reward)
        else:
            uncertainty = sqrt(self.param*tam_item*(successes+failures))
            reward = successes/(successes + failures)
            actions = [ItemBandit(item, value = reward + uncertainty, count = successes+failures, reward = reward, uncertainty = uncertainty) for item in splitter.item_set]
        return sorted(actions)

    def update_item_info(self, item, count, reward, criteria):
        super().update_item_info(item, count, reward, criteria)
        item.uncertainty = sqrt(self.param*np.log10(self.time)/item.count)
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

class ThompsonSamplingBandit(Bandit):
    """
    """
    def __init__(self, splitter, criteria="mean", count_no_rating = True, alpha = 1, beta = 1):
        self.alpha = alpha
        self.beta = beta
        super().__init__(splitter, criteria = criteria, alpha = alpha, beta = beta, count_no_rating = count_no_rating)

    def update_item_info(self, item, count, reward, criteria):
        super().update_item_info(item, count, reward, criteria)
        item.value = item.reward
        item.successes += reward

    def select_item(self, splitter, user):
        # Generate a random number following a beta distribution for each item
        sample = []
        for item in self.actions:
            num = np.random.beta(item.successes + self.alpha, item.count - item.successes + self.beta)
            sample.append((num, item))

        sample = sorted(sample, reverse=True)
        i = 0
        item = sample[i][1]
        while user in splitter.train_set.keys() and item.item in splitter.train_set[user]:
            i += 1
            item = sample[i][1]
        self.actions.remove(item)
        return item

if __name__=="__main__":
    from splitter import Splitter, PercentageSplitter

    spl = Splitter("../data/ratings_binary.txt", " ")
    bandit = UCBBandit(spl)
    bandit.output_to_file("../results/ucb2_epoch_cm100_wmean.txt",
                          "../results/ucb2_recall_cm100_wmean.txt")

    #eps = 0.1
    #spl = Splitter("../data/ratings_binary.txt", " ")
    #bandit = EpsilonGreedyBandit(spl, criteria="cummulative_mean")
    #bandit.output_to_file("../results/eps{0}_epoch_cm100_Rating.txt".format(eps),
    #                      "../results/eps{0}_recall_cm100_Rating.txt".format(eps))

    #spl = Splitter("../data/ratings_binary.txt", " ")
    #bandit = EpsilonGreedyBandit(spl, criteria="cummulative_mean", count_no_rating = False)
    #bandit.output_to_file("../results/eps{0}_epoch_cm100_noRating.txt".format(eps),
    #                      "../results/eps{0}_recall_cm100_noRating.txt".format(eps))

    #spl = Splitter("../data/ratings_binary.txt", " ")
    #bandit = ThompsonSamplingBandit(spl, criteria="cummulative_mean")
    #bandit.output_to_file("../results/ts_epoch_cm100_Rating.txt",
    #                      "../results/ts_recall_cm100_Rating.txt")

    #bandit = ThompsonSamplingBandit(spl, criteria="cummulative_mean", count_no_rating = False)
    #bandit.output_to_file("../results/ts_epoch_cm100_Rating.txt",
    #                      "../results/ts_recall_cm100_Rating.txt")
