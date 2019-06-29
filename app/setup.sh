#!/bin/bash
#
# setup.sh
#
# Sets up python3 venv
#
# NOTE: Requires that python3 is available.
#

VENV_DIR=/tmp/venv3_scraper

virtualenv $VENV_DIR -p python3
source $VENV_DIR/bin/activate

# install dependencies
pip install -r requirements.txt

# this installs the package that is
# defined in setup.py
pip install -e .

# end
