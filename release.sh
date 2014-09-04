#! /bin/bash

source setup.sh
pip install wheel
python2.7 setup.py sdist upload
python2.7 setup.py bdist_wheel upload
python3.3 setup.py bdist_wheel upload