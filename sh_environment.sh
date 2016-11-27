#!/usr/bin/env bash

conda env create -n weka-porter -c defaults python=2 -f environment.yml
source activate weka-porter