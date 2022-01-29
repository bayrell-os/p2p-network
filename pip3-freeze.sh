#!/bin/bash

. env/bin/activate

pip3 freeze > ./requirements.txt
