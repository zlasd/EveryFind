#coding=utf-8
import sys,os
sys.path.append(os.path.abspath('..'))

import logging

logging.basicConfig(level=logging.DEBUG,
	format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
	datefmt='%a, %d %b %Y %H:%M:%S',
	filename='my.log',
	filemode='w')

from flask import Flask
import config

app = Flask(__name__)
app.config.from_object('config')

from app import models,views
