#!/bin/bash
for i in `seq 18 499`
do
    python google_image_search_scrapper.py $i
done
