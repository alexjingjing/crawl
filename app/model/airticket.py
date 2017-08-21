# -*- coding: utf-8 -*-
import pytz
from datetime import datetime

from sqlalchemy import Column, String, BIGINT, INTEGER, TIMESTAMP

from app.model import Base


class AirTicket(Base):
    # 表名
    __tablename__ = 'air_ticket'

    # 表结构
    id = Column(BIGINT, primary_key=True)
    airline_name = Column(String)
    flight_type = Column(String)
    dep_time = Column(String)
    arr_time = Column(String)
    dep_airport = Column(String)
    arr_airport = Column(String)
    price = Column(INTEGER)
    discount = Column(String)
    dep_date = Column(String)
    create_time = Column(TIMESTAMP, default=datetime.now(pytz.timezone('Asia/Shanghai')))
    update_time = Column(TIMESTAMP)

    def __init__(self, airline_name, flight_type, dep_time, arr_time, dep_airport, arr_airport, price, discount,
                 dep_date):
        self.airline_name = airline_name
        self.flight_type = flight_type
        self.dep_time = dep_time
        self.arr_time = arr_time
        self.dep_airport = dep_airport
        self.arr_airport = arr_airport
        self.price = price
        self.discount = discount
        self.dep_date = dep_date

    def __repr__(self):
        return 'airline_name is {}'.format(self.airline_name)
