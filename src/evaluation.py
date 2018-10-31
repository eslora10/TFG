class Evaluation(object):
    """
    """
    def __init__(self, test_len_ini, k, test, recommendation):
        self.test_len_ini = test_len_ini
        self.k = k

        self.hits = 0
        self.coverage = 0
        num_users = 0
        len_reco = 0

        # for user1 in test:
        for user1 in recommendation:
            num_users+=1
            T = set( test[user1].keys() )
            R = recommendation[user1]
            T_R = T.intersection(R)
            self.hits += len( T_R )
            self.coverage += len(R)

        # self.precision = self.hits/( self.k*len(recommendation) )
        # self.recall = self.hits/sum([i for i in self.test_len_ini.values()])
        self.precision=self.hits/( self.k*num_users )
        self.recall=self.hits/self.test_len_ini
        self.coverage/=(self.k*num_users)
