#! /bin/bash
if [ -d venv ]; then rm -rf venv
fi
virtualenv-3.4 venv --python=`which python3.4` --prompt="(eztable)" --clear
source venv/bin/activate
pip install nose
pip install mock
pip install coverage
pip install bintrees
pip install six

