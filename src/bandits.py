# -*- coding: utf-8 -*-
""" Module: bandits

This module implements several multi-armed-bandit algorithms applied to Recommender Systems

Todo:
    * Considerar la opcion de tener train
"""

import numpy as np
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
    def __init__(self, item, value = 0, successes = 0, count = 0, time = 0, reward = 0, uncertainty = 0):
        self.item = item
        self.value = value
        self.count = count
        self.time = time
        self.reward = reward
        self.uncertainty = uncertainty
        self.successes = successes

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

    def __init__(self, splitter, outpath, criteria="mean", count_no_rating = True, social = False, alpha = 0, beta = 0):
        """ Creates a new Bandit and perfoms the algorithm.

        Note:
            This is an abstract class and it should not be instanciated

        Args:
            splitter (:obj: `Splitter`): Object which contains both train and test
            criteria (str or callable, optional): how to compute the reward of an item

        Returns:
            A Bandit object with the iteration finished.

        """
        outfile = open(outpath, "w")
        self.removed = 0
        self.social = social

        self.time = 0
        self.init_items(splitter, alpha, beta)
        self.len_actions = len(self.actions)
        len_test_ini = splitter.test_len
        self.cummulative_recall = [0]
        self.recall = 0
        while splitter.test_set:
            for user in splitter.user_set:
                if user in splitter.test_set.keys():
                    item = self.select_item(splitter, user)
                    # Remove the item from the ordered actions set
                    if item.item in splitter.test_set[user].keys():
                        reward = splitter.test_set[user][item.item]
                        self.update_item_info(item, reward, criteria)
                        # Remove the user from the item_user set
                    else:
                        # In case we don't have info about the item we add it to the train
                        # set with reward=0
                        reward = 0
                        if count_no_rating:
                            self.update_item_info(item, reward, criteria)
                    # Update recall
                    self.recall += reward
                    # Update train and test
                    self.update_train_test(splitter, user, item, reward)
                    # Reinsert the item in its new position
                    if not self.removed:
                        insort(self.actions, item)
                    self.removed = 0
                self.time += 1
            #self.cummulative_recall.append(recall/len_test_ini)
            outfile.write("{0}\n".format(self.recall/len_test_ini))
            #print(len(self.actions))
        outfile.close()

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
        if self.social:
            try:
                splitter.test_set[item.item].pop(user)
                if not splitter.test_set[item.item]:
                    splitter.test_set.pop(item.item)
                #self.recall += 1
            except:
                pass
        # Insert the item in the train_set
        try:
            splitter.train_set[user][item.item] = reward
        except KeyError:
            splitter.train_set[user] = {item.item: reward}

        try:
            splitter.item_users[item.item].pop(user)
            if not splitter.item_users[item.item]:
                item.time = self.time
                self.actions.remove(item)
        except ValueError:
            self.removed = 1
        except KeyError:
            pass
        if self.social:
            try:
                splitter.item_users[user].pop(item.item)
                if not splitter.item_users[user]:
                    self.actions.remove(ItemBandit(user))
            except ValueError:
                pass
            except KeyError:
                pass

    def init_items(self, splitter, alpha, beta):
        """ Creates the ItemBandit list to use during the algorithm.

        Args:
            splitter (:obj: `Splitter`): Object which contains both train and test

        Returns:
            A sorted list which contains the ItemBanit objects.

        """
        count = alpha + beta
        if count != 0:
            reward = alpha/count
        else:
            reward = 0
        self.actions =  sorted([ItemBandit(item, successes = alpha, count = count, reward = reward) for item in splitter.item_users.keys()]) #splitter.item_set])


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

    def update_item_info(self, item, reward, criteria):
        """ Updates the item information each time an item has been chosen

        Args:
        item (:obj: `ItemBandit`):

        Returns:
            None

        """
        item.successes += reward
        item.count += 1
        if criteria == "mean":
            item.reward = item.successes /item.count
        elif criteria == "cummulative_mean":
            item.reward = 1/2*(item.reward + reward)
        else:
            item.reward = criteria(item.reward, reward)

    def follow_back(self, splitter, item, user):
        """ In a social network dataset, checks if the item is following the user

        Args:
            splitter (:obj: `Splitter`): Object which contains both train and test
            item (int): item to check
            user (int): user to check
        """
        if self.social:
            return item == user or item in splitter.train_set.keys() and user in splitter.train_set[item]
        else:
            return False

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

    def __init__(self, splitter, outpath, epsilon=0.1, criteria="mean", count_no_rating = False, social = False, alpha = 0, beta = 0):
        self.epsilon = epsilon
        super().__init__(splitter, outpath, criteria=criteria, count_no_rating = count_no_rating, social=social, alpha = alpha, beta = beta)

    def select_item(self, splitter, user):
        # Check if we have info about the item and if we haven't reccomended the item
        # before to the same user

        if np.random.binomial(1, 1-self.epsilon):
            # Exploitation
            i = 0
            item = self.actions[i]
            while user in splitter.train_set.keys() and item.item in splitter.train_set[user]\
                  or self.follow_back(splitter, item.item, user):
                i+=1
                item = self.actions[i]
        else:
            # Exploration
            #item = random.sample(self.actions, 1)[0]
            i = np.random.randint(len(self.actions))
            item = self.actions[i]
            while user in splitter.train_set.keys() and item.item in splitter.train_set[user]\
                  or self.follow_back(splitter, item.item, user):
                #item = random.sample(self.actions, 1)[0]
                i = np.random.randint(len(self.actions))
                item = self.actions[i]
        self.actions.pop(i)
        return item

    def update_item_info(self, item, reward, criteria):
        super().update_item_info(item, reward, criteria)
        item.value = item.reward

class UCBBandit(Bandit):

    def __init__(self, splitter,outpath,  criteria="mean", param=2, count_no_rating = False, social = False, alpha = 0, beta = 0):
        self.param = param
        super().__init__(splitter, outpath, criteria=criteria, count_no_rating = count_no_rating, social = social, alpha = alpha, beta = beta)

    def init_items(self, splitter, alpha, beta):
        tam_item = len(splitter.item_set)
        count = alpha + beta + 1
        uncertainty = sqrt(self.param*np.log10(tam_item*count)) # After doing this initialation this would be the uncertainty
        self.time = tam_item*count
        self.actions = []
        items = list(splitter.item_set)
        users = list(splitter.user_set)
        tam_users = len(users)
        for i in range(tam_item):
            item = items[i]
            user = users[i%tam_users]
            val = 0
            if item in splitter.test_set[user].keys():
                val = splitter.test_set[user][item]
            reward = (val + alpha)/count
            # TODO: MIRAR ACIERTOS
            itemb = ItemBandit(item, value = reward + uncertainty, count = count, reward = reward, uncertainty = uncertainty, successes = alpha)
            self.actions.append(itemb)
            self.update_train_test(splitter, user, itemb, reward)
        #self.actions = sorted(self.actions)

    def update_item_info(self, item, reward, criteria):
        super().update_item_info(item, reward, criteria)

        for item2 in self.actions:
            item2.uncertainty = sqrt(self.param*np.log10(self.time)/item2.count)
            item2.value = item2.reward + item2.uncertainty
        #self.actions = sorted(self.actions)

    """
    def select_item(self, splitter, user):
        i = 0
        item = self.actions[i]
        while user in splitter.train_set.keys() and item.item in splitter.train_set[user]:
            i += 1
            item = self.actions[i]
        self.actions.pop(i)
        return item
    """
    def select_item(self, splitter, user):
        max_item = self.actions[0]
        for item in self.actions[1:]:
            if not (user in splitter.train_set.keys() and item.item in splitter.train_set[user]\
                    or self.follow_back(splitter, item.item, user)):
                if item.value > max_item.value:
                   max_item = item
        self.removed = 1
        return max_item

class ThompsonSamplingBandit(Bandit):
    """
    """
    def __init__(self, splitter,outpath,  criteria="mean", alpha = 1, beta = 1, count_no_rating = True, social = False):
        self.alpha = alpha
        self.beta = beta
        super().__init__(splitter,outpath,  criteria, count_no_rating = count_no_rating, social = social)

    def update_item_info(self, item, reward, criteria):
        super().update_item_info(item, reward, criteria)
        item.value = item.reward

    """
    def select_item(self, splitter, user):
        # Generate a random number following a beta distribution for each item
        sample = []
        for item in self.actions:
            num = np.random.beta(item.successes + 1, item.count - item.successes + 1)
            sample.append((num, item))

        sample = sorted(sample, reverse=True)
        i = 0
        item = sample[i][1]
        while user in splitter.train_set.keys() and item.item in splitter.train_set[user]:
            i += 1
            item = sample[i][1]
        self.actions.remove(item)
        return item
    """
    def select_item(self, splitter, user):
        max_item = self.actions[0]
        max_val = np.random.beta(max_item.successes + self.alpha, max_item.count - max_item.successes + self.beta)
        for item in self.actions[1:]:
            if not (user in splitter.train_set.keys() and item.item in splitter.train_set[user])\
                    or self.follow_back(splitter, item.item, user):
                val = np.random.beta(item.successes + self.alpha, item.count - item.successes + self.beta)
                if val > max_val:
                    max_item = item
                    max_val = val
        self.removed = 1
        return max_item

if __name__=="__main__":
    from splitter import Splitter
    from plot import plot_results_graph
    import matplotlib.pyplot as plt

    spl = Splitter("../data/interactions-graph-200tweets_no_reps.tsv", separator='\t', social = True)
    bandit = EpsilonGreedyBandit(spl, "prueba", social = True)
    print(len(bandit.actions))
    plot_results_graph("prueba", "ucb")
    plt.show()
