#coding=utf-8
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Text,DateTime,ForeignKey,Table,Float,Enum,desc,Boolean,func
from sqlalchemy.orm import relationship,backref
from flask import url_for
from app import app
from datetime import datetime
import math

Base=declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	username = Column(String(30), nullable=False,unique=True, index=True)
	password = Column(String(32), nullable=False)
	nickname = Column(String(30))
	student_id = Column(String(30))
	student_name = Column(String(30))
	role = Column(Enum('admin','authen_user','unanthen_user'))
	contact_type = Column(Enum('QQ','WeChat','phone','email'))
	contact_way = Column(String(30))
	create_time = Column(DateTime, default=datetime.now)

	is_authenticated = True
	is_active = True
	is_anonymous = False

	def __init__(self, username, password, nickname, student_id, student_name, role, contact_type, contact_way):
		self.username = username
		self.password = password
		self.nickname = nickname
		self.student_id = student_id
		self.student_name = student_name
		self.role = role
		self.contact_type = contact_type
		self.contact_way = contact_way
		self.create_time = datetime.now()

	def __repr__(self):
		return '<User %s>' % self.username

class Lost_record(Base):
	__tablename__ = 'lost_record'

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'))
	type = Column(Enum('student card','credit card','else'))
	description = Column(Text)
	is_end = Column(Boolean, default=False)
	section1 = Column(String(30))
	section2 = Column(String(30))
	section3 = Column(String(30))
	create_time = Column(DateTime, default=datetime.now)


	user = relationship('User', backref=backref('lost_records', order_by=desc(create_time)))

	def __init__(self, user_id, type, description, is_end=False, section1='', section2='', section3=''):
		self.user_id = user_id
		self.type = type
		self.description = description
		self.is_end = is_end
		self.section1 = section1
		self.section2 = section2
		self.section3 = section3
		self.create_time = datetime.now()

	def __repr__(self):
		return '<Lost %d>' % id

class Pick_record(Base):
	__tablename__ = 'pick_record'

	id = Column(Integer, primary_key=True)
	type = Column(Enum('student card','credit card','else'))
	description = Column(Text)
	pic_name = Column(String(10))
	contact_type = Column(Enum('QQ','WeChat','phone','email'))
	contact_way = Column(String(30))
	is_end = Column(Boolean, default=False)
	section1 = Column(String(30))
	section2 = Column(String(30))
	section3 = Column(String(30))
	create_time = Column(DateTime, default=datetime.now)

	def __init__(self, type, description, pic_name, contact_type, contact_way, is_end=False, section1='', section2='', section3=''):
		self.type = type
		self.description = description
		self.pic_name = pic_name
		self.contact_type = contact_type
		self.contact_way = contact_way
		self.is_end = is_end
		self.section1 = section1
		self.section2 = section2
		self.section3 = section3
		self.create_time = datetime.now()

	def __repr__(self):
		return '<Pick %d>' % id

class Claim_record(Base):
	__tablename__ = 'claim_record'

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'))
	pick_record_id = Column(Integer, ForeignKey('pick_record.id'))
	create_time = Column(DateTime, default=datetime.now)

	user = relationship('User', backref=backref('claim_records', order_by=desc(create_time)))
	pick_record = relationship('Pick_record', backref=backref('claim_records', order_by=desc(create_time)))

	def __init__(self, user_id, pick_record_id):
		self.user_id = user_id
		self.pick_record_id = pick_record_id
		self.create_time = datetime.now()

	def __repr__(self):
		return '<Claim %s %d>' % use
