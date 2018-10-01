awk '{ if($3<=2) {$3=0} else {$3=1}; gsub("  ",/\t/); print}' ../data/ratings.txt > ../data/ratings_binary.txt
