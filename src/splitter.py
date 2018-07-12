import numpy as np

class Splitter(object):
    """

    """

    train = {}
    train_r = {}
    test = {}
    test_r = {}

    def __init__(self, datapath):

        self.data = open(datapath, 'r')

class TimestampSplitter(Splitter):
    """

    """
    def __init__(self, datapath, timestamp):

        super().__init__(datapath)
        self.timestamp = timestamp

        # Removes the data head
        self.data.readline()

        # Start reading the data file line by line
        for line in self.data:

            inter = line.split('\t')

            if inter[0] != inter[1]:

                # If the line matches our timestamp we add the interaction to our
                # train set
                if int(inter[2]) <= self.timestamp:

                    try:
                        self.train[int(inter[0])].add(int(inter[1]))
                    except KeyError:
                        self.train[int(inter[0])] = set([int(inter[1])])

                    try:
                        self.train_r[int(inter[1])].add(int(inter[0]))
                    except:
                        self.train_r[int(inter[1])] = set( [ int(inter[0]) ] )

                # If the line does't match the timestamp we add it to the test
                # set
                elif (int( inter[0] ) not in self.train.keys() or int( inter[1] ) not in self.train[int(inter[0])])\
                and (int( inter[1] ) not in self.train.keys() or int( inter[0] ) not in self.train[int(inter[1])])\
                and (int( inter[1] ) not in self.test.keys() or int( inter[0] ) not in self.test[int(inter[1])]):
                    # TODO
                    try:
                        self.test[int(inter[0])].add(int(inter[1]))
                    except KeyError:
                        self.test[int(inter[0])] = set([int(inter[1])])

                    try:
                        self.test_r[int(inter[1])].add(int(inter[0]))
                    except:
                        self.test_r[int(inter[1])] = set( [ int(inter[0]) ] )
        self.data.close()

class RandomSplitter(Splitter):
    """

    """
    def __init__(self, datapath, p):

        super().__init__(datapath)
        self.p = p

        # Removes the data head
        self.data.readline()

        # Start reading the data file line by line
        for line in self.data:

            inter = line.split('\t')

            if inter[0] != inter[1]:

                # Generates a random number following a bernoulli distribution
                if np.random.binomial(1, self.p):

                    try:

                        self.train[int(inter[0])].add(int(inter[1]))

                    except KeyError:

                        self.train[int(inter[0])] = set([int(inter[1])])

                elif (int( inter[0] ) not in self.train.keys() or int( inter[1] ) not in self.train[int(inter[0])])\
                and (int( inter[1] ) not in self.train.keys() or int( inter[0] ) not in self.train[int(inter[1])])\
                and (int( inter[1] ) not in self.test.keys() or int( inter[0] ) not in self.test[int(inter[1])]):
                    # TODO
                    try:

                        self.test[int(inter[0])].add(int(inter[1]))

                    except KeyError:

                        self.test[int(inter[0])] = set([int(inter[1])])
        self.data.close()

if __name__ == "__main__":
    # spl = TimestampSplitter("../data/interactions-graph-200tweets.tsv", 1310147215000)
    # spl = TimestampSplitter("../data/prueba.tsv", 3)
    spl = RandomSplitter("../data/interactions-graph-200tweets.tsv", 0.2)
    print ("TRAIN SET:")
    print (len( spl.train ))
    print ("TEST SET:")
    print ( len( spl.test ))
