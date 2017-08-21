# -*- coding: utf-8 -*-

import pytz
from datetime import datetime
from sqlalchemy import Column, String, BIGINT, TIMESTAMP

from app.model import Base


class DepArr(Base):
    # 表名
    __tablename__ = 'dep_arr'

    dep_city = Column(String, primary_key=True)
    arr_city = Column(String, primary_key=True)
    date_type = Column(BIGINT)
    create_time = Column(TIMESTAMP, default=datetime.now(pytz.timezone('Asia/Shanghai')))
    update_time = Column(TIMESTAMP)

    def __init__(self, dep_city, arr_city, date_type=1):
        self.dep_city = dep_city
        self.arr_city = arr_city
        self.date_type = date_type

    def __repr__(self):
        return 'the dep_city is {} and arr_city is {}'.format(self.dep_city, self.arr_city)


class DateType(Base):
    # 表名
    __tablename__ = 'date_type'

    id = Column(BIGINT, primary_key=True)
    day_gap = Column(String)

    def __init__(self, day_gap):
        self.day_gap = day_gap

    def __repr__(self):
        return 'day gap is {}'.format(self.day_gap)
