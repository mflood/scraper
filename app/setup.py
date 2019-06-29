#!/usr/bin/env python
#
# setup.py
#
# this is installed while in the venv
# with:
#
#   pip install -e .
# 
# (which is called from setup.sh)
#
from distutils.core import setup

setup(name='scraper',
      version='1.0',
      description='Scrape Website',
      author='Matthew Flood',
      author_email='matthew.data.flood@gmail.com',
      url='https://www.github.com/mflood/scraper',
      packages=['scraper'],
      install_requires=[
          'requests',
          'requests-html',
          'bs4',
      ],
     )
