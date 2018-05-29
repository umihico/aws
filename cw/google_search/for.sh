#!/bin/bash
for i in `seq 19 476`
do
    python google_image_search_scrapper.py $i
done
