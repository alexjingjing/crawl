# -*- coding: utf-8 -*-
import pytz
from datetime import datetime

from sqlalchemy import Column, String, BIGINT, SMALLINT, INTEGER, TIMESTAMP

from app.model import Base


class AirTicketIe(Base):
    # 表名
    __tablename__ = 'air_ticket_ie'

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
    dep_city = Column(String)
    arr_city = Column(String)
    dep_city_code = Column(String)
    arr_city_code = Column(String)
    duration = Column(String)
    is_transfer = Column(SMALLINT)
    transfer_city = Column(String)
    ticket_status = Column(String)
    tax_price = Column(INTEGER)
    ticket_price = Column(INTEGER)

    def __init__(self, airline_name, flight_type, dep_time, arr_time, dep_airport, arr_airport, price, discount,
                 dep_date, dep_city, arr_city, dep_city_code, arr_city_code, duration, is_transfer, transfer_city,
                 ticket_status, tax_price, ticket_price):
        self.airline_name = airline_name
        self.flight_type = flight_type
        self.dep_time = dep_time
        self.arr_time = arr_time
        self.dep_airport = dep_airport
        self.arr_airport = arr_airport
        self.price = price
        self.discount = discount
        self.dep_date = dep_date
        self.dep_city = dep_city
        self.arr_city = arr_city
        self.dep_city_code = dep_city_code
        self.arr_city_code = arr_city_code
        self.duration = duration
        self.is_transfer = is_transfer
        self.transfer_city = transfer_city
        self.ticket_status = ticket_status
        self.tax_price = tax_price
        self.ticket_price = ticket_price

    def __repr__(self):
        return 'airline_name is {}'.format(self.airline_name)
