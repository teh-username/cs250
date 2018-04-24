#!/bin/bash

for i in {1..3}
do
  docker run tehusername/sysbench sysbench memory --memory-total-size=3700G --memory-block-size=1M --report-interval=1 --threads=4 --time=60 run >> data.log 2>&1 &
  echo 'Sleeping...'
  sleep 15s
  echo 'Running noisy neighbor 1'
  docker run tehusername/stress stress --vm 1 -t 45 &
  echo 'Running noisy neighbor 2'
  docker run tehusername/stress stress --vm 1 -t 45 &
  echo 'Running noisy neighbor 3'
  docker run tehusername/stress stress --vm 1 -t 45 &
  echo 'Running noisy neighbor 4'
  docker run tehusername/stress stress --vm 1 -t 45 &
  echo 'Running noisy neighbor 5'
  docker run tehusername/stress stress --vm 1 -t 45
done

