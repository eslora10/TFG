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
        self.max_item = 0
        self.max_item_value = 0

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
                            if not splitter.test_set[user]:
                                splitter.test_set.pop(user)
                            try:
                                splitter.train_set[user][item] = reward
                            except KeyError:
                                splitter.train_set[user] = {item: reward}
                            break

    def select_item(self, splitter):
        pass

    def plot_hist(self):
        sns.set()
        N = len(self.actions.keys())
        X = list(self.actions.keys())
        Y1 = [self.actions[action]["count"] for action in self.actions.keys()]
        Y2 = [self.actions[action]["value"] for action in self.actions.keys()]
        fig, (f1, f2) = plt.subplots(2, 1)
        f1.bar(range(N), Y1, tick_label = X)
        f1.set_title("Number of times selected")
        f2.bar(range(N), Y2, tick_label = X)
        f2.set_title("Estimated value")
        plt.show()

class EpsilonGreedyBandit(Bandit):
    """
    """

    def __init__(self, epsilon, splitter, criteria="mean"):
        self.epsilon = epsilon
        super().__init__(splitter, criteria=criteria)

    def select_item(self, splitter):
        if np.random.binomial(1, 1-self.epsilon):
            # Eploitation
            item = self.max_item
        else:
            # Exploration
            item = random.sample(splitter.item_set, 1)[0]
        return item


if __name__=="__main__":
    from splitter import Splitter

    spl = Splitter("../data/ratings_binary.txt", " ")
    bandit = EpsilonGreedyBandit(0.1, spl)
    bandit.plot_hist()
