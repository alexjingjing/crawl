# -*- coding: utf-8 -*-
import sys

from app.tasks.crawl import crawl_task, crawl_task_ie
from app.utils.dbutil import *
from app.utils.randomutil import get_rand_int


def crawl_ie_with_cities(dep_city, arr_city):
    city_result = get_ie_cities_to_crawl_with_cities(dep_city, arr_city)
    for city in city_result:
        crawl_task_ie.apply_async((city[0], city[1], city[2], city[3], city[4]),
                                  count_down=get_rand_int())


if __name__ == '__main__':
    crawl_ie_with_cities('上海', '柬埔寨')
    result = []
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    if len(mode) > 0 and mode != 'all':
        print('invalid param, try \'python entry.py all\' instead!')
        exit(1)
    elif mode == 'all':
        result = get_cities_to_crawl()
    else:
        result = get_cities_to_crawl_with_offset()
    for city_info in result:
        crawl_task.apply_async((city_info[0], city_info[1], city_info[2]), count_down=get_rand_int())
