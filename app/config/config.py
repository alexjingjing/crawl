# -*- coding: utf-8 -*-
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

base_url = "https://sjipiao.fliggy.com/flight_search_result.htm?" \
           + "searchBy={}tripType=0&depCityName={}&depCity=&" \
           + "arrCityName={}&arrCity=&depDate={}&arrDate="

base_url_ie = "https://sijipiao.fliggy.com/ie/flight_search_result.htm?" \
              + "searchBy={}&_input_charset=utf-8&tripType=0&depCityName={}&depCity=&" \
              + "arrCityName={}&arrCity=&arrDate=&depDate={}"

# PHANTOMJS_PATH = "/home/siming.liu/phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
PHANTOMJS_PATH = "/Users/liusiming/phantomjs/phantomjs-2.1.1-macosx/bin/phantomjs"
dcap = dict(DesiredCapabilities.PHANTOMJS)
