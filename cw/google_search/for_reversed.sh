#!/bin/bash
for i in `seq 476 19 -1`
do
    python google_image_search_scrapper.py $i
    git add results.txt
    git commit -m "result check $i"
    git push
done
