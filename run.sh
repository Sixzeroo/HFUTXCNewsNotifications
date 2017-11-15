#!/bin/bash

BASIC_DIR='your_basicdir'
VIRTUAL_DIR='your_virtualdir'

source /home/ubuntu/py_env/web_me/bin/activate

cd $BASIC_DIR
python web_info.py
