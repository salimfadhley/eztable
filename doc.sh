#! /bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/src
source setup.sh
pip install sphinx
cd $DIR/src/doc
make clean
make html
cd $DIR
python setup.py upload_docs
cd $DIR