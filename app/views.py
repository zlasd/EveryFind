#coding=utf-8

from flask import session,g,request
from flask import render_template,url_for,redirect,flash,abort
from flask import jsonify
from app import app
from models import *
from functions import *
import os
import md5
import math
import logging

myMap = {
'QQ' : u"QQ", 'WeChat' : u"微信",
'phone' : u"手机", 'email' : u"邮箱",
'student card' : (u'校园卡', u"学号", u"姓名", u"地点"),
'credit card' : (u"银行卡", u"银行", u"卡号后4位", u"地点"),
'else' : (u"其他", u"类型", u"地点", u"时间")
}


@app.route('/')
@app.route('/index')
def page_index():
	#return 'Hello,world!'
	try:
		pick_records = g.session.query(Pick_record).order_by(Pick_record.create_time.desc()).limit(20).all()
		lost_records = g.session.query(Lost_record).order_by(Lost_record.create_time.desc()).limit(20).all()
	except Exception, e:
		logging.error(str(e))
		print e
		abort(500)

	return render_template('index.html', user=g.user, title=u'主页-'+app.config['MAIN_TITLE'], pick_records=pick_records[:5], lost_records=lost_records[:5], myMap=myMap)

@app.route('/pick_list')
def page_pick_list():
	#return 'pick up list page'
	try:
		pick_records = g.session.query(Pick_record).order_by(Pick_record.create_time.desc()).all()
	except Exception, e:
		logging.error(str(e))
		print e
		abort(500)

	return render_template('pick_list.html', user=g.user, title=u'失物认领-'+app.config['MAIN_TITLE'], records=pick_records, myMap=myMap)


@app.route('/lost_list')
def page_lost_list():
	#return 'lost list page'
	try:
		lost_records = g.session.query(Lost_record).order_by(Lost_record.create_time.desc()).all()
	except Exception, e:
		logging.error(str(e))
		print e
		abort(500)

	return render_template('lost_list.html', user=g.user, title=u'寻物启事-'+app.config['MAIN_TITLE'], records=lost_records, myMap=myMap)


@app.route('/pick_info/<int:id>')
def page_pick_info_id(id):
	#return 'pick info of %d' % id
	try:
		recd = g.session.query(Pick_record).get(id)
	except Exception, e:
		abort(404)
	if not recd: abort(404)
	return render_template('pick_info_id.html', user=g.user, title=u'失物信息-'+app.config['MAIN_TITLE'], record=recd, myMap=myMap)


@app.route('/lost_info/<int:id>')
def page_lost_info_id(id):
	#return 'lost info of %d' % id
	try:
		recd = g.session.query(Lost_record).get(id)
	except Exception, e:
		abort(404)
	if not recd: abort(404)
	return render_template('lost_info_id.html', user=g.user, title=u'寻物信息-'+app.config['MAIN_TITLE'], record=recd, myMap=myMap)

@app.route('/pick_new', methods=['GET','POST'])
def page_pick_new():
	#return 'new pick up info'
	if request.method == 'GET':
		return render_template('pick_new.html', user=g.user, title=u'发布失物-'+app.config['MAIN_TITLE'])

	type_ = request.form.get('type')
	description = request.form.get('description')
	contact_type = request.form.get('contact_type')
	contact_way = request.form.get('contact_way')
	section1 = request.form.get('section1')
	section2 = request.form.get('section2')
	section3 = request.form.get('section3')

	attr = (description, contact_way, section1, section2, section3)
	(description, contact_way, section1, section2, section3) = map(myEncode, attr)

	is_end = False
	has_picture = request.files.get('picture') is not None
	pic_name = None if not has_picture else request.files['picture'].filename.split('.')[-1]
	pick_record = Pick_record(type_, description, pic_name, contact_type, contact_way, is_end, section1, section2, section3)
	try:
		g.session.add(pick_record)
		g.session.commit()
	except Exception, e:
		logging.error(str(e))
		print e
		g.session.rollback()
		abort(500)
	else:
		if has_picture:
			file = request.files['picture']
			if file:
				file.save(os.path.join(app.config['PICTURE_DIR'], str(pick_record.id)+'.'+pic_name))
			else:
				logging.warning('%d with no picture' % pick_record.id)
		return redirect(url_for('page_pick_info_id', id=pick_record.id))


@app.route('/lost_new', methods=['GET','POST'])
def page_lost_new():
	#return 'new lost info'
	if request.method == 'GET':
		return render_template('lost_new.html', user=g.user, title=u'发布寻物-'+app.config['MAIN_TITLE'])

	if not session.has_key('id'):
		abort(405)

	user_id = session['id']

	type_ = request.form.get('type')
	description = request.form.get('description')
	contact_type = request.form.get('contact_type')
	contact_way = request.form.get('contact_way')
	section1 = request.form.get('section1')
	section2 = request.form.get('section2')
	section3 = request.form.get('section3')

	attr = (description, contact_way, section1, section2, section3)
	(description, contact_way, section1, section2, section3) = map(myEncode, attr)


	is_end = False

	lost_record = Lost_record(user_id, type_, description, is_end, section1, section2, section3)
	try:
		g.session.add(lost_record)
		g.session.commit()
	except Exception, e:
		logging.error(str(e))
		print e
		g.session.rollback()
		abort(500)
	else:
		return redirect(url_for('page_lost_info_id', id=lost_record.id))

@app.route('/register')
def page_register():
	return 'register page'
	return render_template('register.html', user=g.user, title=u'注册-'+app.config['MAIN_TITLE'])


@app.route('/help')
def page_help():
	return 'help page'
	return render_template('help.html', user=g.user, title=u'帮助-'+app.config['MAIN_TITLE'])


@app.route('/ajax_login', methods=['POST'])
def ajax_login():
	#return 'ajax login request'

	if session.has_key('id'):
		return jsonify(result='-1') #已登录状态

	username = request.form.get('username')
	password = request.form.get('password')
	password = md5.md5(password).hexdigest()

	if g.session.query(User).filter(User.username==username).count() == 0:
		return jsonify(result='1') #用户名不存在
	elif g.session.query(User).filter(User.username==username,User.password==password).count() == 0:
		return jsonify(result='2') #密码不正确
	else:
		user = g.session.query(User).filter(User.username==username,User.password==password).one()
		session['id'] = user.id
		return jsonify(result='0') #登录成功


@app.route('/ajax_logout', methods=['POST'])
def ajax_logout():
	#return 'ajax logout request'

	if not session.has_key('id'):
		return jsonify(result='-1') #未登录状态

	session.pop('id')
	return jsonify(result='0') #登出成功


@app.route('/ajax_register', methods=['POST'])
def ajax_register():
	#return 'ajax register request'

	#前端需要一个表单认证:长度,字符集合等

	username = request.form.get('username')
	password = request.form.get('password')
	password = md5.md5(password).hexdigest()
	nickname = request.form.get('nickname')
	student_id = request.form.get('student_id')
	student_name = request.form.get('student_name')
	contact_type = request.form.get('contact_type')
	contact_way = request.form.get('contact_way')

	role = 'authen_user'
	attr = (nickname, student_name)
	(nickname, student_name) = map(myEncode, attr)

	if g.session.query(User).filter(User.username==username).count() > 0:
		return jsonify(result='1') #用户名已存在
	else:
		user = User(username, password, nickname, student_id, student_name, role, contact_type, contact_way)
		try:
			g.session.add(user)
			g.session.commit()
		except Exception, e:
			logging.error(str(e))
			print e
			g.session.rollback()
			return jsonify(result='-1') #注册失败
		else:
			session['id'] = user.id
			return jsonify(result='0') #注册成功


@app.route('/ajax_ask_contact', methods=['POST'])
def ajax_ask_contact():
	return 'ajax ask contact request'

	if not session.has_key('id'):
		return jsonify(result='1') #未登录

	pick_record_id = int(request.form.get('pick_record_id'))
	try:
		pick_record = g.session.query(Pick_record).get(pick_record_id)
	except:
		abort(404)

	claim_record = Claim_record(session['id'], pick_record_id)
	try:
		g.session.add(claim_record)
		g.session.commit()
	except Exception, e:
		logging.error(str(e))
		print e
		g.session.rollback()
		return jsonify(result='-1') #失败

	return jsonify(result='0', contact_type=pick_record.contact_type, contact_way=pick_record.contact_way) #成功


@app.errorhandler(404)
def error_404(error):
	return render_template('error.html', user=g.user, title='404:Not found', error=u'没有找到这个页面'), 404


@app.errorhandler(403)
def error_403(error):
	return render_template('error.html', user=g.user, title='403:Forbidden', error=u'页面可能被和谐了'), 403


@app.errorhandler(405)
def error_405(error):
	return render_template('error.html', user=g.user, title='405:Forbidden', error=u'你的打开方式有问题'), 405


@app.errorhandler(400)
def error_400(error):
	return render_template('error.html', user=g.user, title='400:Bad Request', error=u'服务器没法理解这个请求'), 400


@app.errorhandler(500)
def error_500(error):
	return render_template('error.html', user=g.user, title='500:Internal Server Error', error=u'服务器异常'), 500


@app.route('/favicon.ico')
def favicon():
	return redirect(url_for('static', filename='img/favicon.ico'))
