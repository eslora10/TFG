
if __name__ == "__main__":
    from splitter import TimestampSplitter, RandomSplitter
    import time
    from evaluation import Evaluation
    from addition import HitAddition
    from strategy import UniformRandomStrategy

    # i=0
    # spl = RandomSplitter("../data/interactions-graph-200tweets_100.tsv", 0.1)
    # spl = TimestampSplitter("../data/interactions-graph-200tweets_100k.tsv", 1357685061000)
    spl = TimestampSplitter("../data/interactions-graph-200tweets.tsv", 1357685061000)
    # spl = TimestampSplitter("../data/interactions-graph-200tweets_100.tsv",1310147215000 )
    k = 10
    s = UniformRandomStrategy(spl)
    ev = Evaluation(spl.test_len_ini,k )
    ad = HitAddition()
    before = 0
    pr = open("../results/precision.txt", "a")
    rc = open("../results/recall.txt", "a")
    hit = open("../results/hits.txt", "a")
    cov = open("../results/coverage.txt", "a")
    # while before != spl.train_len:
    for i in range(1000):
        # print('--------TRAIN SET--------')
        # print( spl.train )
        # print( spl.train_len )
        before = spl.train_len
        # print('--------TEST SET--------')
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
        print("%d\t%f " % ( i, ev.precision ), file=pr)
        print("%d\t%f " % ( i, ev.recall ), file=rc)
        print("%d\t%d " % ( i, ev.hits ), file=hit)
        print("%d\t%f " % ( i, ev.coverage ), file=cov)
        # i+=1
        ad.add(spl, reco)
