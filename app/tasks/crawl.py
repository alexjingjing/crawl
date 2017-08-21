# -*- coding: utf-8 -*-
import time
from celery.signals import task_success, task_failure
from celery.utils.log import get_task_logger
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.model import session
from app.model.airticket import AirTicket
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
            EC.presence_of_element_located((By.CLASS_NAME, 'flight-list-box'))
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
