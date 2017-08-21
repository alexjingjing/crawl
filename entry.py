# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from app.tasks.crawl import crawl_task
from app.utils.dbutil import *
from app.utils.randomutil import get_rand_int

if __name__ == '__main__':
    result = get_cities_to_crawl()
    for city_info in result:
        dep_arr = city_info[0]
        day_gap = city_info[1].day_gap
        day_gap_list = eval('[' + day_gap + ']')
        for gap in day_gap_list:
            dep_date = str(datetime.today() + timedelta(days=gap))[0:10]
            crawl_task.apply_async((dep_arr.dep_city, dep_arr.arr_city, dep_date), count_down=get_rand_int())
