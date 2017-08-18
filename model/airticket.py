# -*- coding: utf-8 -*-
from mongoengine import Document
from mongoengine import StringField, IntField


class AirTicket(Document):
    airline_name = StringField()
    flight_type = StringField()
    dep_time = StringField()
    arr_time = StringField()
    dep_airport = StringField()
    arr_airport = StringField()
    price = IntField()
    discount = StringField()
    dep_date = StringField()
