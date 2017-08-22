# -*- coding: utf-8 -*-
import sys

from app.tasks.crawl import crawl_task
from app.utils.dbutil import *
from app.utils.randomutil import get_rand_int

if __name__ == '__main__':
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
