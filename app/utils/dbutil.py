# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from sqlalchemy import and_

from app.model import Session
from app.model.airticket import AirTicket
from app.model.deparr import DepArr, DateType
from app.model.deparrie import DepArrIe
from app.model.exceptionlog import ExceptionLog
from app.model.crawllog import CrawlLog, SUCCESS, FAIL


def get_cities_to_crawl():
    result = []
    session = Session()
    cities = session.query(DepArr).all()
    for dep_arr in cities:
        day_gap = get_date_type_by_id(dep_arr.date_type).day_gap
        day_gap_list = eval('[' + day_gap + ']')
        for gap in day_gap_list:
            dep_date = str(datetime.today() + timedelta(days=gap))[0:10]
            if session.query(CrawlLog).filter(and_(
                            CrawlLog.dep_city == dep_arr.dep_city,
                            CrawlLog.arr_city == dep_arr.arr_city,
                            CrawlLog.dep_date == dep_date,
                            CrawlLog.create_time >= datetime.today() - timedelta(days=1),
                            CrawlLog.create_time <= datetime.today())).first() is None:
                result.append((dep_arr.dep_city, dep_arr.arr_city, dep_date))
    session.close()
    return result


def get_cities_to_crawl_with_offset(offset=0, limit=10):
    result = []
    session = Session()
    cities = session.query(DepArr).offset(offset).limit(limit)
    for dep_arr in cities:
        day_gap = get_date_type_by_id(dep_arr.date_type).day_gap
        day_gap_list = eval('[' + day_gap + ']')
        for gap in day_gap_list:
            dep_date = str(datetime.today() + timedelta(days=gap))[0:10]
            if session.query(CrawlLog).filter(and_(
                            CrawlLog.dep_city == dep_arr.dep_city,
                            CrawlLog.arr_city == dep_arr.arr_city,
                            CrawlLog.dep_date == dep_date,
                            CrawlLog.create_time >= datetime.today() - timedelta(days=1),
                            CrawlLog.create_time <= datetime.today())).first() is None:
                result.append((dep_arr.dep_city, dep_arr.arr_city, dep_date))
    if len(result) == 0:
        result = get_cities_to_crawl_with_offset(offset + 1, limit)
    session.close()
    return result


def get_cities_to_crawl_with_cities(dep_city, arr_city):
    result = []
    session = Session()
    dep_arr = session.query(DepArr).filter(and_(DepArr.dep_city == dep_city,
                                                DepArr.arr_city == arr_city)).first()
    if dep_arr is not None:
        day_gap = get_date_type_by_id(dep_arr.date_type).day_gap
        day_gap_list = eval('[' + day_gap + ']')
        for gap in day_gap_list:
            dep_date = str(datetime.today() + timedelta(days=gap))[0:10]
            result.append((dep_city, arr_city, dep_date))
    session.close()
    return result


def get_ie_cities_to_crawl_with_cities(dep_city, arr_city):
    result = []
    session = Session()
    dep_arr_ie = session.query(DepArrIe).filter(and_(DepArrIe.dep_city == dep_city,
                                                     DepArrIe.arr_city == arr_city)).first()
    if dep_arr_ie is not None:
        day_gap = get_date_type_by_id(dep_arr_ie.date_type).day_gap
        day_gap_list = eval('[' + day_gap + ']')
        for gap in day_gap_list:
            dep_date = str(datetime.today() + timedelta(days=gap))[0:10]
            result.append((dep_city, arr_city, dep_arr_ie.dep_city_code, dep_arr_ie.arr_city_code, dep_date))
    session.close()
    return result


def get_date_type_by_id(date_type_id):
    session = Session()
    result = session.query(DateType).filter(DateType.id == date_type_id).first()
    session.close()
    return result


def save_exception_log(exception_info):
    session = Session()
    try:
        session.add(ExceptionLog(exception_info[0], exception_info[1]))
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()


def save_crawl_log(dep_city, arr_city, dep_date, status, search_by):
    session = Session()
    try:
        session.add(CrawlLog(dep_city, arr_city, dep_date, status, search_by))
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()
