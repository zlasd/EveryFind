#coding=utf-8
import os

CSRF_ENABLED=True
SECRET_KEY='ljhandlwt'

DATABASE_NAME = 'EveryFind'
DB_CONNECT_STRING = 'mysql://admin:admin@127.0.0.1/%s' % DATABASE_NAME

PICTURE_DIR = os.path.join(os.path.abspath('.'),'app','static','img','picture')

MAIN_TITLE = 'EveryFind'