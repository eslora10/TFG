class Addition(object):
    """
    """
    def add(self, splitter, recommendation):
        self.run(splitter, recommendation)
        splitter.train_len = sum([len(s) for s in splitter.train.values()])
        splitter.test_len = sum([len(s) for s in splitter.test.values()])

    def run(self, splitter, recommendation):
        pass

class TopKAddition(Addition):
    """
    """
    def run(self, splitter, recommendation):
        # For each user we get the interactions set. For the train set,
        # we add all top k interactions the recommendation has given.
        # For the test set we remove them.
        for user1 in splitter.train:
            splitter.train[user1] = splitter.train[user1].union(recommendation[user1])
            splitter.test[user1] = splitter.test[user1].difference(recommendation[user1])


class HitAddition(Addition):
    """
    """
    def run(self, splitter, recommendation):
        for user1 in splitter.train:
            T_R = splitter.test[user1].intersection(recommendation[user1])
            splitter.train[user1] = splitter.train[user1].union(T_R)
            splitter.test[user1] = splitter.test[user1].difference(T_R)
