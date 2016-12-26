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

myMap = {
'QQ' : u"QQ", 'WeChat' : u"微信",
'phone' : u"手机", 'email' : u"邮箱",
'student card' : (u'校园卡', u"学号", u"姓名", u"地点"),
'credit card' : (u"银行卡", u"银行", u"卡号后4位", u"地点"),
'else' : (u"其他", u"类型", u"地点", u"时间")
}
