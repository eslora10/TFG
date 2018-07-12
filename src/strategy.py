import numpy as np

class Strategy(object):
    """

    """
    users  = set()

    def __init__(self, datapath):
        with open(datapath, 'r') as data:
            data.readline()
            for line in data:
                user = int( line.split('\t')[0] )
                self.users.add(user)
            data.close()

    def strategy(self):
        return {}

    def process(self, k):
        test_p = {}
        weights = self.strategy()
        for user in weights.keys():
            weights[user].sort(key=lambda x: x[1], reverse=True)
            test_p[user] = [user2[0] for user2 in weights[user][:k]]
        return test_p

class UniformRandomStrategy(Strategy):

    def strategy(self):
        weights = {}
        for user1 in self.users:
            weights[user1] = []
            for user2 in self.users:
                if user1 != user2:
                    weights[user1].append((user2, np.random.uniform()))
        return weights


if __name__ == "__main__":
    s = UniformRandomStrategy("../data/interactions-graph-200tweets_100.tsv")
    print( s.process(10) )
