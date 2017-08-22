# -*- coding: utf-8 -*-
from app.tasks.crawl import crawl_task
from app.utils.dbutil import *
from app.utils.randomutil import get_rand_int

if __name__ == '__main__':
    result = get_cities_to_crawl_with_offset()
    for city_info in result:
        crawl_task.apply_async((city_info[0], city_info[1], city_info[2]), count_down=get_rand_int())
