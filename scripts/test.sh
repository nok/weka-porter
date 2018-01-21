#!/usr/bin/env bash

source activate weka-porter
python -m unittest discover -vp '*Test.py'
source deactivate