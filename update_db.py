#coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app
from app.models import *

engine = create_engine(app.config['DB_CONNECT_STRING'], echo=False)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()
Base.metadata.create_all(engine)

#session.execute('alter table loj add signature varchar(200) not null default %s;' % u'这个人很懒,什么都没写...'.encode('utf-8'))
#p = Problem('Hello,world!', 'Print the string "Hello,world!"', sample_output='Hello,world!')
#session.add(p)
#session.commit()
