class Addition(object):
    """
    """
    def add(self, splitter, recommendation):
        self.run(splitter, recommendation)
        splitter.train_len = sum([len(s) for s in splitter.train.values()])
        splitter.test_len = sum([len(s) for s in splitter.test.values()])

    def run(self, splitter, recommendation):
        pass

class HitAddition(Addition):
    """
    """
    def run(self, splitter, recommendation):
        for user1 in splitter.train:
            hits = splitter.test[user1].intersection(recommendation[user1])
            misses = recommendation[user1].difference(hits)
            splitter.train[user1] = splitter.train[user1].union(hits)
            splitter.test[user1] = splitter.test[user1].difference(hits)
            splitter.train_miss[user1] = splitter.train_miss[user1].union(misses)
