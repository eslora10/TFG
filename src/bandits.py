import numpy as np
import random

class Bandit(object):
    """
    """
    k = 1 # Number of items to recommend
    def __init__(self, exploit_algorithm, splitter):
        self.exploit_algorithm = exploit_algorithm
        self.splitter = splitter
        self.reco_items = []
        self.is_bandit = []

    def exploitation(self):
        """
        """
        pass

    def random_sample_filter(self, user, item_set, k):
        sample = set()
        i = 0
        while i<k:
            item = random.sample(item_set, 1)[0]
            if ( item not in self.splitter.train[user] and user not in self.splitter.train_r[item] )\
                and (user != item) and (item not in self.splitter.train_miss[user])\
                and item not in sample:
                sample.add(item)
                i+=1
        return sample

    def process(self, T):
        """
        """
        #TODO: Check whether the selected item has been recommended before
        for _ in range(T):
            # Random select user from the train set
            user = random.sample(self.splitter.train.keys(), 1)
            if self.exploitation():
                # If the bandit selects exploitation we use the recommender
                # algorithm to select k items for the user
                # self.reco_items.append(list( self.exploit_algorithm.recommend(self.k, user).items()) )
                self.reco_items.append( self.exploit_algorithm.recommend(self.k, user) )
                self.is_bandit.append(False)
            else:
                # Otherwise we get k random items
                self.reco_items.append( {u: self.random_sample_filter(u, self.splitter.train_r.keys(), self.k ) for u in user} )
                self.is_bandit.append(True)

class EpsilonGreedyBandit(Bandit):
    """ Selects the best leveler arm with probability 1-eps
    """
    def __init__(self, exploit_algorithm, splitter, eps):
        """
        """
        self.eps = eps
        Bandit.__init__(self, exploit_algorithm, splitter)

    def exploitation(self):
        """
        """
        return np.random.binomial(1, 1-self.eps)

if __name__ == "__main__":
    from splitter import PercentageSplitter
    from algorithms import PopularityAlgorithm

    spl = PercentageSplitter("../data/interactions-graph-200tweets.tsv",0.2)

    alg = PopularityAlgorithm(spl)
    bandit = EpsilonGreedyBandit(alg, spl, 0.2)
    bandit.process(10)
    print(bandit.reco_items)
    print(bandit.is_bandit)
