#!/bin/bash

for i in {1..3}
do
  docker run tehusername/sysbench sysbench memory --memory-total-size=3700G --memory-block-size=1M --report-interval=1 --threads=4 --time=60 run >> data.log 2>&1 &
  echo 'Sleeping'
  sleep 60
#  echo 'Running noisy neighbor'
#  docker run tehusername/stress stress --vm 4 -t 60
done

