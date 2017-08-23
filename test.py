# -*- coding: utf-8 -*-

import time

from bs4 import BeautifulSoup
from app.model import Session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.model.airticket import AirTicket
from app.model.airticketie import AirTicketIe

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap[
    "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
dcap[
    "phantomjs.page.settings.userAgent"] = \
    "User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) " \
    + "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"

# PHANTOMJS_PATH = "E:\Project\Python\phantomjs-2.1.1-windows\\bin\phantomjs.exe"
# PHANTOMJS_PATH = "/home/lsm1993/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
PHANTOMJS_PATH = "/Users/liusiming/phantomjs/phantomjs-2.1.1-macosx/bin/phantomjs"
driver = webdriver.PhantomJS(PHANTOMJS_PATH,
                             desired_capabilities=dcap)

base_url = "https://sjipiao.fliggy.com/flight_search_result.htm?" \
           + "searchBy=1270tripType=0&depCityName={}&depCity=&" \
           + "arrCityName={}&arrCity=&depDate={}&arrDate="

base_url_ie = "https://sijipiao.fliggy.com/ie/flight_search_result.htm?" \
              + "searchBy={}&_input_charset=utf-8&tripType=0&depCityName={}&depCity={}&" \
              + "arrCityName={}&arrCity={}&depDate={}&arrDate="


def test_selenium():
    session = Session()
    dep_city = '上海'
    arr_city = '北京'
    dep_date = '2017-08-21'
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
        print(str(e))
    finally:
        session.close()
        driver.save_screenshot("./test.png")
        driver.quit()


def test_selenium_ie():
    session = Session()
    dep_city = '上海'
    dep_city_code = 'SHA'
    arr_city = '柬埔寨'
    arr_city_code = 'REP'
    dep_date = '2017-08-25'
    dep_city_name = format_city_name(dep_city)
    arr_city_name = format_city_name(arr_city)
    driver.get(base_url_ie.format(1282, dep_city_name, dep_city_code, arr_city_name, arr_city_code, dep_date))
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'J_FlightItem'))
        )
        time.sleep(0.5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        flight_items = soup.find_all("div", class_="J_FlightItem")
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
            print(flight_type, dep_time, dep_airport, arr_time, arr_airport, duration, is_transfer, transfer_city,
                  price, ticket_price, tax_price, ticket_status)
    except Exception as e:
        print(str(e))
    finally:
        session.close()
        driver.save_screenshot("./test.png")
        driver.quit()


def format_city_name(name):
    return ((str(name.encode('GB2312'))[2:-1]).replace('\\x', '%')).upper()


if __name__ == '__main__':
    test_selenium_ie()
