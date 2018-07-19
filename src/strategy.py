import numpy as np

class Strategy(object):
    """

    """

    def __init__(self, splitter):
        self.splitter = splitter

    def strategy(self):
        return {}

    def process(self, k):
        test_p = {}
        weights = self.strategy()
        for user in weights.keys():
            weights[user].sort(key=lambda x: x[1], reverse=True)
            test_p[user] = set( user2[0] for user2 in weights[user][:k] )
        return test_p

class UniformRandomStrategy(Strategy):

    def strategy(self):
        weights = {}
        for user1 in self.splitter.train.keys():
            weights[user1] = []
            for user2 in self.splitter.train.keys():
                if user1 != user2:
                    weights[user1].append((user2, np.random.uniform()))
        return weights


if __name__ == "__main__":
    from splitter import TimestampSplitter
    import time
    ini = time.time()
    spl = TimestampSplitter("../data/interactions-graph-200tweets_100.tsv", 1307039324000)
    # spl = TimestampSplitter("../data/prueba.tsv", 4)
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
    print( len( s.process(10)) )
    print ( time.time()-ini )
