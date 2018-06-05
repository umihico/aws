#!/bin/bash -eu
while read line
do
  set -- $line
  filename = $1$(basename $3)
  curl -o $filename $3 
  $filename >> progress.txt
done < ./urls.txt
