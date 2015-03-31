#!/bin/sh

while sleep 1;
do
  for i in `seq 1 78`;do
    python ./rgb.py $i
    sleep 1
  done
done
