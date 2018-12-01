import numpy as np

class Splitter(object):
    """

    """
    def __init__(self, path, separator='\t'):
        self.train_len = 0
        self.test_len = 0
        self.user_set = set()
        self.item_set = set()
        self.train_set = {}
        self.test_set = {}

        with open(path) as data:
            for line in data:
                inter = line.split(separator)
                user = int(inter[0])
                item = int(inter[1])
                value = int(inter[2])
                self.user_set.add(user)
                self.item_set.add(item)
                if self.condition():
                    try:
                        if item not in self.train_set[user].keys():
                            self.train_set[user][item] = value
                    except KeyError:
                        self.train_set[user] = {item: value}
                    self.train_len += 1
                else:
                    try:
                        if item not in self.test_set[user].keys():
                            self.test_set[user][item] = value
                    except KeyError:
                        self.test_set[user] = {item: value}
                    self.test_len += 1


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
    def __init__(self, path, prob):
        self.prob = prob
        super().__init__(path)

    def condition(self):
        return np.random.binomial(1, self.prob)

class PercentageSplitter(Splitter):
    """
    """
    def __init__(self, path, percentage):
        self.percentage = percentage
        super().__init__(path)

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
