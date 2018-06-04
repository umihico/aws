#!/bin/bash
while read line
do
  set -- $line
  fname=$1$(basename $3)
  echo $fname
  echo $3
  curl -o $fname "${3%$'\r'}"
done < ./urls.txt
