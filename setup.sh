#! /bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source bin/activate
cd $DIR/src
python setup.py develop