import numpy as np

class Splitter(object):
    """

    """

    train = {}
    train_miss = {}
    train_len = 0
    train_len_p = 0
    train_len_ini = {}
    train_r = {}
    test = {}
    test_len = 0
    test_len_p = 0
    test_len_ini = 0
    test_r = {}

    def __init__(self, datapath, arg):

        self.data = open(datapath, 'r')

        # Removes the data head
        self.data.readline()

        # Start reading the data file line by line
        for line in self.data:

            inter = line.split('\t')
            user1 = int( inter[0] )
            user2 = int( inter[1] )
            if user1 != user2:

                # If the line matches our timestamp we add the interaction to our
                # train set
                if self.condition(arg, int(inter[2])):

                    try:
                        self.train[user1].add(user2)
                    except KeyError:
                        self.train[user1] = set([user2])
                    self.train_len_p+=1
                    if user2 not in self.train:
                        self.train[user2] = set()

                    if user2 not in self.test:
                        self.test[user2] = set()

                    if user1 not in self.test:
                        self.test[user1] = set()
                    try:
                        self.train_r[user2].add(user1)
                    except:
                        self.train_r[user2] = set( [ user1 ] )


                # If the line does't match the timestamp we add it to the test
                # set
                elif (user1 not in self.train or user2 not in self.train[user1])\
                and (user2 not in self.train or user1 not in self.train[user2])\
                and (user2 not in self.test or user1 not in self.test[user2]):
                    try:
                        self.test[user1].add(user2)
                    except KeyError:
                        self.test[user1] = set([user2])
        #                self.test_len+=1

                    self.test_len_p+=1
                    if user2 not in self.test:
                        self.test[user2] = set()

                    if user2 not in self.train:
                        self.train[user2] = set()

                    if user1 not in self.train:
                        self.train[user1] = set()
                    try:
                        self.test_r[user2].add(user1)
                    except:
                        self.test_r[user2] = set( [ user1 ] )

        self.train_len = sum([len(s) for s in self.train.values()])
        self.test_len = sum([len(s) for s in self.test.values()])
        self.test_len_ini = self.test_len

        for user in self.train:
            self.train_miss[user] = set()

        self.data.close()

    def condtion(self, arg1, arg2):
        return true

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

#TODO: Nuevo splitter que parta el train y el test segun una proporcion exacta dada

class TwoFileSplitter(Splitter):

    def split(self, test_path):
        train = self.data
        test = open(test_path, 'r')
        test.readline()

        for line in test:
            inter = line.split('\t')
            user1 = int( inter[0] )
            user2 = int( inter[1] )
            try:
                self.test[user1].add(user2)
            except KeyError:
                self.test[user1] = set([user2])

            if user2 not in self.test:
                self.test[user2] = set()

            if user2 not in self.train:
                self.train[user2] = set()

            if user1 not in self.train:
                self.train[user1] = set()

            try:
                self.test_r[user2].add(user1)
            except:
                self.test_r[user2] = set( [ user1 ] )

        for line in train:
            inter = line.split('\t')
            user1 = int( inter[0] )
            user2 = int( inter[1] )
            if user1 != user2:
                try:
                    self.train[user1].add(user2)
                except KeyError:
                    self.train[user1] = set([user2])

                if user2 not in self.train:
                    self.train[user2] = set()

                if user2 not in self.test:
                    self.test[user2] = set()

                if user1 not in self.test:
                    self.test[user1] = set()
                try:
                    self.train_r[user2].add(user1)
                except:
                    self.train_r[user2] = set( [ user1 ] )
        test.close()


if __name__ == "__main__":
    # spl = TimestampSplitter("../data/interactions-graph-200tweets.tsv", 1357685061000)
    # spl = TimestampSplitter("../data/prueba.tsv", 3)
    spl = RandomSplitter("../data/interactions-graph-200tweets_100.tsv", 0.2)
    print ("TRAIN SET:")
    print (spl.train)
    print (spl.train_len)
    print (spl.train_len_p)
    print ("TEST SET:")
    print (spl.train)
    print (spl.test_len)
    print (spl.test_len_p)
