for i in 0 0.01 0.1 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1
do
    p=$(head -1782 "eps"$i"_epoch_cm100_wmean.txt" | tail -1)
    echo "$i,$p"
done
