for file in `\find . / zips - name '*.zip'`
do sh 001_unzip_dir_htm_and_images.sh $file
done
