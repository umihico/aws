for file in `\find . -type f \(-name '*.jpg' - o - name '*.png' - o - name '*.gif' \)`
do echo $file >> 002_image_paths.csv
done
