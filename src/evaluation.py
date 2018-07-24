class Evaluation(object):
    """
    """
    def __init__(self, len_test_ini, k):
        self.len_test_ini = len_test_ini
        self.k = k

    def evaluate(self, test, recommendation):
        tp = 0
        num_users = 0
        # tn = 0
        # fp = 0
        # fn = 0
        self.precision = 0
        self.recall = 0
        ttp = 0
        for user1 in test:
            num_users+=1
            T = test[user1]
            R = recommendation[user1]
            T_R = T.intersection(R)
            tp = len( T_R )
            # fp += len( R.difference(T_R))
            # fn += len( T.difference(T_R))
            self.precision += tp/self.k
            try:
             self.recall += tp/self.len_test_ini[user1]
            except ZeroDivisionError:
             pass

        # self.precision = tp/( self.k*len(recommendation) )
        # self.recall = tp/sum([i for i in self.len_test_ini.values()])
        self.precision/=num_users
        self.recall/=num_users
