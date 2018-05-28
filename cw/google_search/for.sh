#!/bin/bash
for i in `seq 16 499`
do
    python google_image_search_scrapper.py $i
done
