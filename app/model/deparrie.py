# -*- coding: utf-8 -*-

import pytz
from datetime import datetime
from sqlalchemy import Column, String, BIGINT, TIMESTAMP

from app.model import Base


class DepArrIe(Base):
    # 表名
    __tablename__ = 'dep_arr_ie'

    dep_city = Column(String, primary_key=True)
    arr_city = Column(String, primary_key=True)
    date_type = Column(BIGINT)
    create_time = Column(TIMESTAMP, default=datetime.now(pytz.timezone('Asia/Shanghai')))
    update_time = Column(TIMESTAMP)
    dep_city_code = Column(String)
    arr_city_code = Column(String)

    def __init__(self, dep_city, arr_city, dep_city_code, arr_city_code, date_type=1):
        self.dep_city = dep_city
        self.arr_city = arr_city
        self.date_type = date_type
        self.dep_city_code = dep_city_code,
        self.arr_city_code = arr_city_code

    def __repr__(self):
        return 'the dep_city is {} and arr_city is {}'.format(self.dep_city, self.arr_city)
