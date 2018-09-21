import numpy as np

class Splitter(object):
    """

    """

    train = {}
    train_miss = {}
    train_len = 0
    train_len_ini = {}
    train_r = {}
    test = {}
    test_len = 0
    test_len_p = 0
    train_len_p = 0
    test_len_ini = 0
    test_r = {}

    def addItem(self, user, item, info, destination_set):
        if destination_set == "train":
            set1 = self.train
            set2 = self.test
            length = self.train_len
            set1_r = self.train_r
        else:
            set1 = self.test
            set2 = self.train
            length = self.test_len
            set1_r = self.test_r


        try:
            # if item not in set1[user]:
            set1[user][ item ] = info
            length+=1
        except KeyError:
            set1[user] = { item: info }
            length+=1

        # if item not in set1:
        #     set1[item] = set()

        # if item not in set2:
        #     set2[item] = set()

        if user not in set2:
            set2[user] = {}
        try:
            set1_r[item][ user ] = info
        except:
            set1_r[item] = { user: info }
        return length

    def __init__(self, datapath, arg):

        self.data = open(datapath, 'r')

        # Removes the data head
        self.data.readline()

        # Start reading the data file line by line
        for line in self.data:

            inter = line.split(' ')
            user = int( inter[0] )
            item = int( inter[1] )
            info = int(inter[2])
            if user != item:

                if self.condition(arg,info):
                    self.train_len = self.addItem(user, item, info, "train")

                elif (user not in self.train or item not in self.train[user])\
                and (item not in self.train or user not in self.train[item])\
                and (item not in self.test or user not in self.test[item]):
                    self.test_len = self.addItem(user, item, info, "test")

        self.test_len_ini = self.test_len

        for user in self.train:
            self.train_miss[user] = set()

        self.data.close()

    def condtion(self, arg1, arg2):
        return True

class TimestampSplitter(Splitter):
    """
    """
    def condition(self, timestamp, timestamp_r):
        return timestamp_r <= timestamp

class RandomSplitter(Splitter):
    """

    """
    def condition(self, p, arg):
        return np.random.binomial(1, p)

class PercentageSplitter(Splitter):
    """
    """
    def condition(self, p, arg):
        try:
            return self.train_len/(self.test_len+self.train_len) < p
        except ZeroDivisionError:
            return True

if __name__ == "__main__":
    # spl = TimestampSplitter("../data/interactions-graph-200tweets_100.tsv",1277496627000 )
    # spl = PercentageSplitter("../data/interactions-graph-200tweets.tsv",0.2)
    # spl = PercentageSplitter("../data/prueba.tsv",0.2)
    spl = PercentageSplitter("../data/ratings_binary.txt" ,0.2)
    # spl = TimestampSplitter("../data/prueba.tsv", 3)
    # spl = RandomSplitter("../data/interactions-graph-200tweets_100.tsv", 0.2)
    print ("TRAIN SET:")
    print (spl.train)
    print (spl.train_len)
    print ("TEST SET:")
    print (spl.test)
    print (spl.test_len)
