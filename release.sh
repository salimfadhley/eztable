#! /bin/bash

source setup.sh
pip install wheel
cd src
python3.4 setup.py sdist upload
python3.4 setup.py bdist_wheel upload