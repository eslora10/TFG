class Evaluation(object):
    """
    """
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    def __init__(self, test, recommendation):
        for user1 in test:
            T = test[user1]
            R = recommendation[user1]
            T_R = T.intersection(R)
            self.tp += len( T_R )
            self.fp += len( R.difference(T_R))
            self.fn += len( T.difference(T_R))
        self.precision = self.tp/(self.tp+self.fp)
        self.recall = self.tp/(self.tp+self.fn)
