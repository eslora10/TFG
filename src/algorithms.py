import numpy as np
import time
import heapq as hq

class Algorithm(object):
    """

    """
    HEAP_SIZE = 100

    def __init__(self, splitter):
        self.splitter = splitter

    def strategy(self):
        return {}

    def recommend(self, k, users):
        i=0
        test_p = {}
        weights = self.strategy(users)
        for user in weights:
            l = []
            while len( weights[user] ) != 0:
                l.insert(0,hq.heappop(weights[user])[1])
            test_p[user] = set(l[:k])
        return test_p

class PopularityAlgorithm(Algorithm):
    """
    """

    def strategy(self, users):
        # First we get each user number of interactions and we sort them
        # in reverse order
        ranking = [  ]
        i = 0
        weights = {}
        train_r = self.splitter.train_r
        train_set = self.splitter.train

        for item in train_r:
            pair = (len(self.splitter.train_r[item]), item)
            if i < self.HEAP_SIZE:
                hq.heappush(ranking, pair)
                i+=1
            else:
                if pair[0] >= ranking[0][0]:
                    hq.heappushpop(ranking,pair)
        # For each user we get the recommended list excluding its neighbours
        for user in users:
            weights[user] = []
            for pair in ranking:
                item = pair[1]
                if ( item not in train_set[user] and user not in train_r[item] )\
                   and (user != item) and (item not in self.splitter.train_miss[user]):
                    weights[user].append(pair)
        return weights
