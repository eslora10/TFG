# Primera version del algoritmo MAB segun el paper
# TODO: Adaptar el codigo al modulo strategy
# TODO: A la hora de seleccionar un item, controlar que no se le haya recomendado previamente
# al usuario
# TODO: 
if __name__ == "__main__":
    import random
    from splitter import PercentageSplitter

    spl = PercentageSplitter("../data/interactions-graph-200tweets.tsv",0.2)
    T = 100000
    i = []
    r = 0
    pr = open("../alg1_res.txt", "w")
    def select_arm(u, splitter):
        return random.sample(splitter.train_r.keys(), 1)[0]

    for t in range(T):
        u = random.sample(spl.train.keys(), 1)[0]
        i.append(select_arm(u, spl))
        if i[t] in spl.test[u].keys():
            r += 1
        pr.write("{0}\t{1}\n".format(t,r))
