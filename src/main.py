
if __name__ == "__main__":
    from splitter import TimestampSplitter, RandomSplitter, TwoFileSplitter
    import time
    from evaluation import Evaluation
    from addition import HitAddition
    from strategy import UniformRandomStrategy, MostFamousStrategy

    # i=0
    # spl = RandomSplitter("../data/interactions-graph-200tweets_100.tsv", 0.1)
    # spl = TimestampSplitter("../data/interactions-graph-200tweets_100k.tsv", 1357685061000)
    # spl = TimestampSplitter("../data/interactions-graph-200tweets.tsv", 1357685061000)
    # spl = TwoFileSplitter("../data/sbs200-inter-train.txt", "../data/sbs200-inter-test.txt")
    # spl = TimestampSplitter("../data/interactions-graph-200tweets_100.tsv",1310147215000 )
    k = 10
    s = UniformRandomStrategy(spl)
    # s = MostFamousStrategy(spl)
    ev = Evaluation(spl.test_len_ini,k )
    ad = HitAddition()
    before = 0
    pr = open("../results/07-25-18_random.txt", "w")
    pr.write("iteration\tprecision\trecall\thits\tcoverage\n")
    # while before != spl.train_len:
    for i in range(1000):
        # print('--------TRAIN SET--------')
        # print( spl.train )
        # print( spl.train_len )
        before = spl.train_len
        # print('--------TEST SET--------')
        # print( spl.test_len )
        # print( spl.test )
        # print('--------MISSES--------')
        #  print( spl.train_miss )
        # print( spl.test_len )
        # print('--------TOTAL--------')
        # print( spl.train_len + spl.test_len )
        # print('--------RECOMMENDATION--------')
        reco = s.process(k)
        # print( len(reco) )
        ev.evaluate(spl.test, reco)
        print(i)
        pr.write("%d\t%f\t%f\t%d\t%f\n" % ( i, ev.precision, ev.recall,ev.hits,ev.coverage ))
        # i+=1
        ad.add(spl, reco)
