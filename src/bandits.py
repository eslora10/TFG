import numpy as np
import matplotlib.pyplot as plt
import random
from evaluation import Evaluation

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
        results = []
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
            # Compute precision and recall
            ev = Evaluation(self.splitter.test_len_ini, self.k, self.splitter.test, self.reco_items[-1])
            results.append(ev)

        return results

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

def plot_results(results):
    """
    """
    plt.style.use('seaborn')
    c_prec = [0]
    c_rec = [0]
    t = [0]
    fig, ( prec, rec ) = plt.subplots(2,1)

    for ev in results:
        c_prec.append(c_prec[-1]+ev.precision)
        c_rec.append(c_rec[-1]+ev.recall)
        t.append(t[-1]+1)

    prec.plot(t, c_prec)
    rec.plot(t, c_rec)
    prec.set_ylabel("Cumulated precision")
    prec.set_xlabel("t")

    rec.set_ylabel("Cumulated recall")
    rec.set_xlabel("t")
    plt.show()

if __name__ == "__main__":
    from splitter import PercentageSplitter
    from algorithms import PopularityAlgorithm

    spl = PercentageSplitter("../data/interactions-graph-200tweets.tsv",0.2)

    alg = PopularityAlgorithm(spl)
    bandit = EpsilonGreedyBandit(alg, spl, 0.2)
    results = bandit.process(100)

    plot_results(results)
