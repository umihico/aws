IFS=$'\n'

find . -maxdepth 1 -name './raw_keyword_stat/*.csv' | while read file
do
  ls "${file}"
  # iconv -f utf-16 -t utf-8 $file > "temp.csv"
  # new_name=`cut -f 1 "temp.csv" | sed -n "4p"`.csv
  cp $file './download.csv'
done
# rm "temp.csv"
# find . -name "* *" | rename 's/ /_/g'
