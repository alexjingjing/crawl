# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 初始化数据库连接:
# engine = create_engine('mysql+pymysql://lsm:password@139.196.96.160:3306/air_ticket?charset=utf8',
#                        encoding='utf-8')
# engine = create_engine('mysql+pymysql://lsm1993:password@localhost:3306/air_ticket?charset=utf8',
#                        encoding='utf-8')
engine = create_engine('mysql+pymysql://lsm1993:password@118.190.87.126:3306/air_ticket?charset=utf8',
                       encoding='utf-8')
# 创建DBSession类型:
session = scoped_session(sessionmaker(bind=engine))
