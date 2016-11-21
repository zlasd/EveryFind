#coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import g,session
from models import *
import traceback

def get_sqlsession():
	engine = create_engine(app.config['DB_CONNECT_STRING'], echo=False)
	DB_Session = sessionmaker(bind=engine)
	session = DB_Session()
	return session

@app.before_request
def before_request():
	g.session = get_sqlsession()
	g.user = g.session.query(User).get(int(session['id'])) if session.has_key('id') else None

def myEncode(s):
	if s: return s.encode("utf-8")
	return s

def myDecode(s):
	if s: return s.decode("utf-8")
	return s
