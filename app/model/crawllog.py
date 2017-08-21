# -*- coding: utf-8 -*-
from datetime import datetime

import pytz
from sqlalchemy import Column, String, BIGINT, INTEGER, TIMESTAMP

from app.model import Base

SUCCESS = 1000
FAIL = 1001


class CrawlLog(Base):
    # 表名
    __tablename__ = 'crawl_log'

    id = Column(BIGINT, primary_key=True)
    dep_city = Column(String)
    arr_city = Column(String)
    dep_date = Column(String)
    status = Column(INTEGER)
    search_by = Column(String)
    create_time = Column(TIMESTAMP, default=datetime.now(pytz.timezone('Asia/Shanghai')))
    update_time = Column(TIMESTAMP)

    def __init__(self, dep_city, arr_city, dep_date, status, search_by):
        self.dep_city = dep_city
        self.arr_city = arr_city
        self.dep_date = dep_date
        self.status = status
        self.search_by = search_by

    def __repr__(self):
        return 'dep city is {}'.format(self.dep_city)
