class Addition(object):
    """
    """
    def __init__(self, splitter, recommendation):
        pass

class TopKAddition(Addition):
    """
    """
    def __init__(self, splitter, recommendation):
        super().__init__(splitter, recommendation)
        # For each user we get the interactions set. For the train set,
        # we add all top k interactions the recommendation has given.
        # For the test set we remove them.
        for user1 in self.train:
            k = len(self.recommendation[user1])
            splitter.train[user1].union(self.recommendation[user1])
            splitter.test[user1].difference(self.recommendation[user1])
