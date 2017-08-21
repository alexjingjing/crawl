# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import Column, String, BIGINT, INTEGER, TIMESTAMP

from app.model import Base


class ExceptionLog(Base):
    # 表名
    __tablename__ = 'exception_log'

    id = Column(BIGINT, primary_key=True)
    exception_code = Column(INTEGER)
    exception_info = Column(String)
    create_time = Column(TIMESTAMP, default=datetime.datetime.now)
    update_time = Column(TIMESTAMP)

    def __init__(self, exception_code, exception_info):
        self.exception_code = exception_code
        self.exception_info = exception_info

    def __repr__(self):
        return 'exception info is {}'.format(self.exception_info)
