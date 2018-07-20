
for file in `\find . -type f \(-name '*.htm' \)`
do echo $file >> 004_htmls.csv
done
