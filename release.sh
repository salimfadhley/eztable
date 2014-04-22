#! /bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source ../bin/activate
cd $DIR
pip install wheel
python setup.py sdist upload
python setup.py bdist_wheel upload