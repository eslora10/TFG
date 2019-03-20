file="../results/gridSearch/ucb/cm100k/param/ucb0_recall_cm100_miniwmean.txt"
a=$(wc -l $file)
num_lines=$(echo $a|cut -d' ' -f1)

#for i in {1..10}
#do
#    for j in {1..10}
#do
#    p=$(head -$((num_lines / 2)) "../results/gridSearch/eps/cm100k/optimistic/eps"$i"_"$j".txt" | tail -1)
#    echo "$i,$j,$(echo $p|cut -d' ' -f2)"
#done
#done
for i in 0 0.1 1 2 10 100
do
    p=$(head -$((num_lines / 2)) "../results/gridSearch/ucb/cm100k/param/ucb"$i"_recall_cm100_miniwmean.txt" | tail -1)
    echo "$i,$(echo $p|cut -d' ' -f2)"
done
