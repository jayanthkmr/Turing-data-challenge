#!/usr/bin/env bash

# Directly running it on multiprocessor
chmod +x pycodemetrics/src/eval.py
nohup pycodemetrics/src/eval.py pycodemetrics/url_list.csv &

#Running it on AWS EMR
chmod +x pycodemetrics/src/mrjobeval.py
nohup  pycodemetrics/src/mrjobeval.py pycodemetrics/url_list.csv -r emr -c pycodemetrics/.mrjobconf &