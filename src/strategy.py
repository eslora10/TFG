import numpy as np
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
        test_p = {}
        weights = self.strategy()
        for user in weights.keys():
            # weights[user].sort(key=lambda x: x[1], reverse=True)
            # test_p[user] = set( user2[1] for user2 in weights[user][:k] )
            # test_p[user] = hq.nlargest(k, weights[user])
            test_p[user] = set(user2 for user2 in sorted(weights[user])[:k] )
        return test_p

class UniformRandomStrategy(Strategy):
    """    def strategy(self):
            weights = {}
            for user1 in self.splitter.train.keys():
                weights[user1] = []
                for user2 in self.splitter.train.keys():
                    if user1 != user2:
                        weights[user1].append((user2, np.random.uniform()))
            return weights
    """
    def strategy(self):
        ini = time.time()
        weights = {}
        train_set = self.splitter.train.keys()
        for user1 in train_set:
            i = 0
            weights[user1] = []
            for user2 in train_set:
                if user1 != user2: #TODO: add the neighbours condition
                    pair = ( np.random.uniform(), user2)
                    if i < self.HEAP_SIZE:
                        hq.heappush(weights[user1], pair)
                        i+=1
                    else:
                        if pair[0] >= weights[user1][0][0]:
                            hq.heappushpop(weights[user1],pair)
        print ( time.time()-ini )
        return weights




if __name__ == "__main__":
    from splitter import TimestampSplitter, RandomSplitter
    import time
    # spl = RandomSplitter("../data/antonio.tsv", 0.2)
    spl = TimestampSplitter("../data/interactions-graph-200tweets.tsv", 1357685061000)
    s = UniformRandomStrategy(spl)
    print('--------TRAIN SET--------')
    # print( spl.train )
    print( len( spl.train ) )
    print( spl.train_len )
    print('--------TEST SET--------')
    # print( spl.test )
    print( len( spl.test ) )
    print( spl.test_len )
    print('--------RECOMENDATION--------')
    # print( s.process(10) )
    reco = s.process(10)
    print( len(reco) )
