from random import shuffle
users = set()
with open("interactions-graph-200tweets_no_reps.tsv", "r") as infile:
    for line in infile:
        spl = line.strip("\n").split("\t")
        users.add(int(spl[0]))
        users.add(int(spl[1]))
users = list(users)
print(users[:10])
shuffle(users)
print(users[:10])
users = users[:1000]

outfile = open("interactions-graph-1000u.tsv", "w")
with open("interactions-graph-200tweets_no_reps.tsv", "r") as infile:
    for line in infile:
        spl = line.strip("\n").split("\t")
        user1 = int(spl[0])
        user2 = int(spl[1])
        if user1 in users and user2 in users:
            outfile.write(line)
outfile.close()
