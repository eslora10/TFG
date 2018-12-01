import numpy as np
import time
import heapq as hq

class Strategy(object):
    """

    """
    HEAP_SIZE = 100

    def __init__(self, splitter):
        self.splitter = splitter

    def strategy(self):
        return {}

    def process(self, k):
        i=0
        test_p = {}
        weights = self.strategy()
        for user in weights:
            l = []
            while len( weights[user] ) != 0:
                l.insert(0,hq.heappop(weights[user])[1])
            test_p[user] = set(l[:k])
        return test_p

class UniformRandomStrategy(Strategy):
    """
    """

    def strategy(self):
        weights = {}
        train_set = self.splitter.train
        for user1 in train_set:
            i = 0
            weights[user1] = []
            for user2 in train_set:
                # Checks if both users aren't neighbours in the train set.
                if ( user2 not in train_set[user1] and user1 not in train_set[user2] )\
                   and (user1 != user2) and (user2 not in self.splitter.train_miss[user1]):
                    pair = ( np.random.random(), user2)
                    if i < self.HEAP_SIZE:
                        hq.heappush(weights[user1], pair)
                        i+=1
                    else:
                        if pair[0] >= weights[user1][0][0]:
                            hq.heappushpop(weights[user1],pair)
        return weights

class PopularityStrategy(Strategy):
    """
    """

    def strategy(self):
        # First we get each user number of interactions and we sort them
        # in reverse order
        ranking = [  ]
        i = 0
        weights = {}
        train_r = self.splitter.train_r
        train_set = self.splitter.train

        for user in train_r:
            pair = (len(self.splitter.train_r[user]), user)
            if i < self.HEAP_SIZE:
                hq.heappush(ranking, pair)
                i+=1
            else:
                if pair[0] >= ranking[0][0]:
                    hq.heappushpop(ranking,pair)
        # For each user we get the recommended list excluding its neighbours
        for user1 in train_set:
            weights[user1] = []
            for pair in ranking:
                user2 = pair[1]
                if ( user2 not in train_set[user1] and user1 not in train_set[user2] )\
                   and (user1 != user2) and (user2 not in self.splitter.train_miss[user1]):
                    weights[user1].append(pair)
        return weights

