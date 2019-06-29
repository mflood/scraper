#!/bin/bash
#
# run.sh
#
# Kick off the scraper
#
VENV_DIR=/tmp/venv3_scraper
source $VENV_DIR/bin/activate

#python scraper/page_scraper.py
python scraper/data_puller.py

# end
