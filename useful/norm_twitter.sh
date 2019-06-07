for i in {1..10}
do
    for j in {1..10}
    do
        echo "../results/gridSearch/ucb/twitter/optimistic/ucb"$i"_"$j".txt"
        head -544 "../results/gridSearch/ucb/twitter/optimistic/ucb"$i"_"$j".txt" > "../results/gridSearch/ucb/twitter/optimistic/ucb"$i"_"$j"_cut.txt"
        awk -vmax=$(awk 'max < $1 { max = $1 } END { print max }' "../results/gridSearch/ucb/twitter/optimistic/ucb"$i"_"$j"_cut.txt")     '{print $1 / max}' "../results/gridSearch/ucb/twitter/optimistic/ucb"$i"_"$j"_cut.txt" > "../results/gridSearch/ucb/twitter/optimistic/ucb"$i"_"$j"_norm.txt"
    done
done

#for i in 0.001 0.01 0.1 1.0 2.0 10.0 100.0 #0 0.001 0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1
#do
#    echo $i
#    echo ../results/gridSearch/ucb/twitter/param/ucb$i_norm.txt
#    head -555 "../results/gridSearch/ucb/twitter/param/ucb"$i".txt" > "../results/gridSearch/ucb/twitter/param/ucb"$i"_cut.txt"
#    awk -vmax=$(awk 'max < $1 { max = $1 } END { print max }' "../results/gridSearch/ucb/twitter/param/ucb"$i"_cut.txt")     '{print $1 / max}' "../results/gridSearch/ucb/twitter/param/ucb"$i"_cut.txt" >> "../results/gridSearch/ucb/twitter/param/ucb"$i"_norm.txt"
#done

#for i in 0 0.001 0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1
#do
#    echo $i
#    echo ../results/gridSearch/ucb/twitter/param/ucb$i_norm.txt
#    head -250 "../results/gridSearch/ucb/twitter/param/ucb"$i".txt" > "../results/gridSearch/ucb/twitter/param/ucb"$i"_cut.txt"
#    awk -vmax=$(awk 'max < $1 { max = $1 } END { print max }' "../results/gridSearch/ucb/twitter/param/ucb"$i"_cut.txt")     '{print $1 / max}' "../results/gridSearch/ucb/twitter/param/ucb"$i"_cut.txt" >> "../results/gridSearch/ucb/twitter/param/ucb"$i"_norm.txt"
#done
