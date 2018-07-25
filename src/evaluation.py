class Evaluation(object):
    """
    """
    def __init__(self, test_len_ini, k):
        self.test_len_ini = test_len_ini
        self.k = k

    def evaluate(self, test, recommendation):
        self.hits = 0
        self.coverage = 0
        num_users = 0

        for user1 in test:
            num_users+=1
            T = test[user1]
            R = recommendation[user1]
            T_R = T.intersection(R)
            self.hits += len( T_R )
            self.coverage += len(R)

        # self.precision = self.hits/( self.k*len(recommendation) )
        # self.recall = self.hits/sum([i for i in self.test_len_ini.values()])
        self.precision=self.hits/( self.k*num_users )
        self.recall=self.hits/self.test_len_ini
        self.coverage/=(self.k*num_users)
