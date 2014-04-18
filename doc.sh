#! /bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source ../bin/activate
cd $DIR
python2.7 setup.py develop
cd doc
make clean
make html
cd $DIR
python setup.py upload_docs