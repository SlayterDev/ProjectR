#!/usr/bin/python
import sys
import os
import logging

activate_this = '/home/apps/ProjectR/flask/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/home/apps/ProjectR/")

os.environ['DATABASE_URL'] = 'mysql://apps:Mixmaster1@localhost/apps'

from app import app as application
application.secret_key = 'Theres-poison-in-the-punch-bowl'
