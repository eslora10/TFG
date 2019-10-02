alg="ucb"
dataset="twitter"

file="../results/gridSearch/"$alg"/"$dataset"/optimistic/"$alg"1_1.txt"
a=$(wc -l $file)
num_lines=$(echo $a|cut -d' ' -f1)

for i in {1..10}
do
    for j in {1..10}
do
    p=$(head -$((num_lines / 2)) "../results/gridSearch/"$alg"/"$dataset"/optimistic/"$alg""$i"_"$j"_norm.txt" | tail -1)
    echo "$i,$j,$(echo $p|cut -d' ' -f2)"
done
done
#for i in 0.01 0.1 1 2 10 100
#for i in 0 0.001 0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1
#do
#    p=$(head -$((num_lines / 2)) "../results/gridSearch/"$alg"/"$dataset"/param/"$alg""$i"_norm.txt" | tail -1)
#    echo "$i,$(echo $p|cut -d' ' -f2)"
#done
