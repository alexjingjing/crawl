# -*- coding: utf-8 -*-
import time
from celery.signals import task_success, task_failure
from celery.utils.log import get_task_logger
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.model import Session
from app.model.airticket import AirTicket
from app.model.airticketie import AirTicketIe
from app.model.crawllog import SUCCESS, FAIL
from app.tasks import app
from app.config.config import *
from app.utils.dbutil import *
from app.constant.exceptioninfo import ExceptionInfo

logger = get_task_logger(__name__)


@app.task(name='crawl_task')
def crawl_task(dep_city, arr_city, dep_date, search_by=1280):
    dcap[
        "phantomjs.page.settings.userAgent"] = \
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    driver = webdriver.PhantomJS(PHANTOMJS_PATH, desired_capabilities=dcap)
    driver.get(base_url.format(search_by, format_city_name(dep_city), format_city_name(arr_city), dep_date))
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'J_FlightItem'))
        )
        time.sleep(0.5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        flight_items = soup.find_all("div", class_="flight-list-item")
        if len(flight_items) == 0:
            save_exception_log(ExceptionInfo.WEB_ELEMENT_NOT_FOUND)
            raise Exception('no elements!')
        for flight_item in flight_items:
            airline_name = flight_item.span.string
            flight_item_ps = flight_item.find_all("p")
            airline_types = flight_item_ps[1]
            airline_type = str(airline_types.contents[0]) + str(airline_types.a.string)
            dep_time = flight_item_ps[2].string
            arr_time = flight_item_ps[3].span.string
            dep_airport = flight_item_ps[4].string
            arr_airport = flight_item_ps[5].string
            prices = flight_item.find("td", class_="flight-price")
            price_spans = prices.find_all("span")
            price = price_spans[1].string
            discount = price_spans[2].string
            air_ticket = AirTicket(airline_name, airline_type, dep_time, arr_time, dep_airport, arr_airport, int(price),
                                   discount, dep_date)
            session = Session()
            session.add(air_ticket)
            session.commit()
            session.close()
    except Exception as e:
        einfo = ExceptionInfo.EXCEPTION_OCCURRED
        save_exception_log((einfo[0], einfo[1] + str(e)))
        raise Exception(str(e))
    finally:
        driver.quit()
        return dep_city, arr_city, dep_date, search_by


@app.task(name='crawl_task_ie')
def crawl_task_ie(dep_city, arr_city, dep_city_code, arr_city_code, dep_date, search_by=1281):
    session = Session()
    dcap[
        "phantomjs.page.settings.userAgent"] = \
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    driver = webdriver.PhantomJS(PHANTOMJS_PATH, desired_capabilities=dcap)
    driver.get(base_url_ie.format(1282, format(dep_city), dep_city_code, format(arr_city), arr_city_code, dep_date))
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'flight-list-box'))
        )
        time.sleep(0.5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        flight_items = soup.find_all("div", class_="J_FlightItem")
        if len(flight_items) == 0:
            save_exception_log(ExceptionInfo.WEB_ELEMENT_NOT_FOUND)
            raise Exception('no elements!')
        for flight_item in flight_items:
            flight_info = flight_item.find("div", class_="flight-info")
            airline_name = flight_info.span.string
            flight_type = str(flight_info.find("p", class_="tip-info").string).strip()
            col_time = flight_item.find("td", class_="col-time")
            dep_time = col_time.find_all("p")[0].string
            dep_airport = col_time.find_all("p")[1].string
            time_arrow = col_time.find("div", class_="time-arrow")
            arrow = time_arrow.find("div", class_="arrow")
            transfer_bool = True if arrow.p is not None else False
            transfer_city = str(time_arrow.find("div", class_="transfer-city").string).strip() if transfer_bool else ''
            col_arr_time = flight_item.find("td", class_="col-arr-time")
            arr_time = col_arr_time.find("p", "time-info").string
            if arr_time is None:
                arr_time_element = col_arr_time.find("p", "time-info").contents
                arr_time = str(arr_time_element[0])
            arr_airport = col_arr_time.find_all("p")[1].string
            duration = flight_item.find("td", class_="col-totaltime").p.string
            col_price = flight_item.find("td", class_="col-price")
            price = str(col_price.find("div", class_="total-price").find("span", class_="price-num").contents[1])
            ticket_price = str(col_price.find("div", class_="hide-when-total-price-sort").
                               find("span", class_="price-num").contents[1])
            tax_price = str(col_price.find("div", class_="hide-when-total-price-sort").
                            find("span", class_="tax-price").contents[2])
            col_select = flight_item.find("td", class_="col-select")
            ticket_status = col_select.find("div", class_="quantity").string \
                if col_select.find("div", class_="quantity") is not None else ''
            is_transfer = 1 if transfer_bool else 0
            air_ticket_ie = AirTicketIe(airline_name, flight_type, dep_time, arr_time, dep_airport, arr_airport,
                                        int(price), '暂无字段',
                                        dep_date, dep_city, arr_city, dep_city_code, arr_city_code, duration,
                                        is_transfer,
                                        transfer_city, ticket_status, int(tax_price), int(ticket_price))
            session.add(air_ticket_ie)
            session.commit()
            session.close()
    except Exception as e:
        einfo = ExceptionInfo.EXCEPTION_OCCURRED
        save_exception_log((einfo[0], einfo[1] + str(e)))
        raise Exception(str(e))
    finally:
        driver.quit()
        return dep_city, arr_city, dep_date, search_by


def format_city_name(name):
    return ((str(name.encode('GB2312'))[2:-1]).replace('\\x', '%')).upper()


@task_success.connect()
@app.task(name='crawl_success')
def crawl_success(sender=None,
                  result=None,
                  **kwargs):
    name = sender.name
    logger.info('[TASK]:{} success!'.format(name))
    save_crawl_log(result[0], result[1], result[2], SUCCESS, result[3])


@task_failure.connect()
@app.task(name='crawl_failure')
def crawl_failure(sender=None,
                  task_id=None,
                  exception=None,
                  args=None,
                  traceback=None,
                  einfo=None,
                  **kwargs):
    name = sender.name
    logger.info('[TASK]:{} failed! info is {}'.format(name, str(einfo)))
    save_crawl_log(args[0], args[1], args[2], FAIL, args[3])
