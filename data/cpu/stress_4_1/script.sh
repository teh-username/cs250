#!/bin/bash


for i in {1..3}
do
  docker run tehusername/sysbench sysbench cpu --cpu-max-prime=20000 --report-interval=1 --threads=4 --time=60 run >> data.log 2>&1 &
  echo 'Sleeping...'
  sleep 15s
  echo 'Running noisy neighbor'
  docker run tehusername/stress stress -c 4 -t 45
done
