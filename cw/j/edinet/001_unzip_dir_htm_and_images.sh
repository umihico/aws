filename=$1
extract_path=$(dirname $filename)/$(basename $filename | sed 's/\.[^\.]*$//')
mkdir $extract_path
unzip -o $filename XbrlSearchDlInfo.csv -d $extract_path
iconv -f MS_KANJI -t UTF-8 $extract_path/XbrlSearchDlInfo.csv > 001_dirlist_in_zip.csv
python 001_list_only_startswith_E.py
sed -i 's/\r//' 001_ok_dirlist_in_zip.csv
for file in $(cat 001_ok_dirlist_in_zip.csv|xargs)
do
  unzip -o  $filename $file/XBRL/PublicDoc/{*.htm,*/*.{jpg,jpeg,gif,png}} -d $extract_path
done
