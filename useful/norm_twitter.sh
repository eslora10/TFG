for i in 0 0.001 0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1
do
    echo $i
    echo ../results/gridSearch/eps/twitter/param/eps$i_norm.txt
    awk -vmax=$(awk 'max < $1 { max = $1 } END { print max }' "../results/gridSearch/eps/twitter/param/eps"$i".txt")     '{print $1 / max}' "../results/gridSearch/eps/twitter/param/eps"$i".txt" >> "../results/gridSearch/eps/twitter/param/eps"$i"_norm.txt"
done
