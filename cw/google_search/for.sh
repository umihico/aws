#!/bin/bash
for i in `seq 1 500`
do
    python google_image_search_scrapper.py $i
done
