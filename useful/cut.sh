file="../results/gridSearch/eps/cm100k/optimistic/eps1_1.txt"
a=$(wc -l $file)
num_lines=$(echo $a|cut -d' ' -f1)

for i in {1..10}
do
    for j in {1..10}
do
    p=$(head -$((num_lines / 2)) "../results/gridSearch/eps/cm100k/optimistic/eps"$i"_"$j".txt" | tail -1)
    echo "$i,$j,$(echo $p|cut -d' ' -f2)"
done
done
