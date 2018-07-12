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

    def process(self):
        pass

class UniformRandomStrategy(Strategy):
    weights = {}

    def strategy(self):
        for user1 in self.users:
            self.weights[user1] = []
            for user2 in self.users:
                if user1 != user2:
                    self.weights[user1].append((user2, np.random.uniform()))
        print(self.weigths)


if __name__ == "__main__":
    s = UniformRandomStrategy("../data/interactions-graph-200tweets.tsv")
    s.strategy()
