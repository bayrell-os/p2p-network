#!/bin/bash

SCRIPT=$(readlink -f $0)
BASEPATH=`dirname "$SCRIPT"`

python3 -m venv ./env

. env/bin/activate

#curl https://bootstrap.pypa.io/get-pip.py | python
#pip install wheel
#python setup.py bdist_wheel

pip install -r ./requirements.txt --find-links=./packages --no-index
