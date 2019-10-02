import numpy as np
from copy import deepcopy

class Splitter(object):
    """

    """
    def __init__(self, path, separator='\t', social = False):
        self.train_len = 0
        self.test_len = 0
        self.user_set = set()
        self.item_set = set()
        self.train_set = {}
        self.test_set = {}
        self.item_users = {}

        with open(path) as data:
            for line in data:
                inter = line.split(separator)
                user = int(inter[0])
                item = int(inter[1])
                value = int(inter[2])
                if social:
                    value = 1 # In datasets from twitter the last value is the timestamp
                self.user_set.add(user)
                self.item_set.add(item)
                if item != user:
                    if item not in self.item_users:
                        self.item_users[item] = {user: value} #self.item_users[item] = set([user])
                    else:
                        self.item_users[item][user] = value #self.item_users[item].add(user)

                    if self.condition():
                        try:
                            if item not in self.train_set[user].keys():
                                self.train_set[user][item] = value
                        except KeyError:
                            self.train_set[user] = {item: value}
                        if value:
                            self.train_len += 1
                    else:
                        try:
                            if item not in self.test_set[user].keys():
                                self.test_set[user][item] = value
                                if item not in self.test_set or user not in self.test_set[item].keys():
                                    self.test_len += value
                        except KeyError:
                            self.test_set[user] = {item: value}
                            if item not in self.test_set or user not in self.test_set[item].keys():
                                self.test_len += value
            if social:
                # In social networks both item and users are the same
                self.user_set = self.user_set.union(self.item_set)
                self.item_set = deepcopy(self.user_set)


    def condition(self):
        """
        """
        return False

# class TimestampSplitter(Splitter):
#     """
#     """
#     def condition(self, timestamp, timestamp_r):
#         return timestamp_r <= timestamp

class RandomSplitter(Splitter):
    """

    """
    def __init__(self, path, prob, separator='\t'):
        self.prob = prob
        super().__init__(path, separator)

    def condition(self):
        return np.random.binomial(1, self.prob)

class PercentageSplitter(Splitter):
    """
    """
    def __init__(self, path, percentage, separator='\t'):
        self.percentage = percentage
        super().__init__(path, separator)

    def condition(self):
        try:
            return self.train_len/(self.test_len+self.train_len) < self.percentage
        except ZeroDivisionError:
            return True

if __name__ == "__main__":
    spl = Splitter("../data/ratings_binary_mini.txt", " ")
    print(spl.train_set)
    print(spl.test_set)
    print(spl.user_set)
    print(spl.item_set)
