# -*- coding: utf-8 -*-
from sqlalchemy import and_

from app.model import session
from app.model.airticket import AirTicket
from app.model.deparr import DepArr, DateType
from app.model.exceptionlog import ExceptionLog
from app.model.crawllog import CrawlLog, SUCCESS, FAIL


def get_cities_to_crawl():
    cities = session.query(DepArr).limit(5)
    for dep_arr in cities:
        if session.query(CrawlLog).filter(and_(CrawlLog.dep_city == dep_arr.dep_city,
                                               CrawlLog.status == FAIL)).first() is not None:
            cities.remove(dep_arr)
            continue
    result = []
    for dep_arr in cities:
        result.append((dep_arr, get_date_type_by_id(dep_arr.date_type)))
    session.close()
    return result


def get_date_type_by_id(date_type_id):
    result = session.query(DateType).filter(DateType.id == date_type_id).first()
    session.close()
    return result


def save_exception_log(exception_info):
    session.add(ExceptionLog(exception_info[0], exception_info[1]))
    session.commit()


def save_crawl_log(dep_city, arr_city, dep_date, status, search_by):
    session.add(CrawlLog(dep_city, arr_city, dep_date, status, search_by))
    session.commit()
