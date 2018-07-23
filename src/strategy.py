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
        for user in weights:
            test_p[user] = set(user2[1] for user2 in sorted(weights[user])[:k] )
        return test_p

class UniformRandomStrategy(Strategy):
    """
    """

    def strategy(self):
        ini = time.time()
        weights = {}
        train_set = self.splitter.train
        for user1 in train_set:
            i = 0
            weights[user1] = []
            for user2 in train_set:
                # Checks if both users aren't neighbours in the train set.
                if ( user2 not in train_set[user1] and user1 not in train_set[user2] ) and (user1 != user2):
                    pair = ( np.random.uniform(), user2)
                    if i < self.HEAP_SIZE:
                        hq.heappush(weights[user1], pair)
                        i+=1
                    else:
                        if pair[0] >= weights[user1][0][0]:
                            hq.heappushpop(weights[user1],pair)
        # print ("TIME: %s" % ( time.time()-ini ) )
        return weights




if __name__ == "__main__":
    from splitter import TimestampSplitter, RandomSplitter
    import time
    from evaluation import Evaluation
    from addition import TopKAddition

    # spl = RandomSplitter("../data/interactions-graph-200tweets_100.tsv", 0.1)
    # spl = TimestampSplitter("../data/interactions-graph-200tweets.tsv", 1357685061000)
    spl = TimestampSplitter("../data/interactions-graph-200tweets_100.tsv",1310147215000 )
    before = 0
    while before != spl.train_len:
        s = UniformRandomStrategy(spl)
        # print('--------TRAIN SET--------')
        # print( spl.train )
        # print( spl.train_len )
        before = spl.train_len
        # print('--------TEST SET--------')
        # print( spl.test )
        # print( spl.test_len )
        # print('--------TOTAL--------')
        # print( spl.train_len + spl.test_len )
        # print('--------RECOMMENDATION--------')
        reco = s.process(10)
        # print( len(reco) )
        ev = Evaluation(spl.test, reco, spl.test_len_ini,10 )
        print("PRECISION: %f " % ev.precision)
        print("RECALL: %f" % ev.recall )


        ad = TopKAddition(spl, reco)
