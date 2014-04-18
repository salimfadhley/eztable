#! /bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source ../bin/activate
cd $DIR
python setup.py install
cd doc
make html
cd $DIR
python setup.py upload_docs