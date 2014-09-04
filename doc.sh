#! /bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/src/doc
make clean
make html
cd $DIR/src
python setup.py upload_docs
cd $DIR