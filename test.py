# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup

from model.airticket import AirTicket

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap[
    "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
# PHANTOMJS_PATH = "E:\Project\Python\phantomjs-2.1.1-windows\\bin\phantomjs.exe"
# PHANTOMJS_PATH = "/home/lsm1993/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
PHANTOMJS_PATH = "/Users/liusiming/phantomjs/phantomjs-2.1.1-macosx/bin/phantomjs"
driver = webdriver.PhantomJS(PHANTOMJS_PATH,
                             desired_capabilities=dcap)

base_url = "https://sjipiao.fliggy.com/flight_search_result.htm?" \
           + "searchBy=1280tripType=0&depCityName={}&depCity=&" \
           + "arrCityName={}&arrCity=&depDate={}&arrDate="


def test_selenium():
    dep_city = '上海'
    arr_city = '北京'
    dep_date = '2017-08-19'
    dep_city_name = format_city_name(dep_city)
    arr_city_name = format_city_name(arr_city)
    driver.get(base_url.format(dep_city_name, arr_city_name, dep_date))
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'flight-list-box'))
        )
        time.sleep(0.5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        flight_items = soup.find_all("div", class_="flight-list-item")
        for flight_item in flight_items:
            airline_name = flight_item.span.string
            flight_item_ps = flight_item.find_all("p")
            airline_types = flight_item_ps[1]
            airline_type = str(airline_types.contents[0]) + str(airline_types.a.string)
            dep_time = flight_item_ps[2].string
            arr_time = flight_item_ps[3].string
            dep_airport = flight_item_ps[4].string
            arr_airport = flight_item_ps[5].string
            prices = flight_item.find("td", class_="flight-price")
            price_spans = prices.find_all("span")
            price = price_spans[1].string
            discount = price_spans[2].string
            air_ticket = AirTicket(airline_name=airline_name, flight_type=airline_type, dep_time=dep_time,
                                   arr_time=arr_time, dep_airport=dep_airport, arr_airport=arr_airport,
                                   price=int(price), discount=discount, dep_date=dep_date)
            air_ticket.save()
    except Exception as e:
        print(str(e))
    finally:
        driver.save_screenshot("./test.png")
        driver.quit()


def format_city_name(name):
    return ((str(name.encode('GB2312'))[2:-1]).replace('\\x', '%')).upper()


if __name__ == '__main__':
    test_selenium()
