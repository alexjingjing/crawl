# -*- coding: utf-8 -*-

from enum import Enum, unique


@unique
class ExceptionInfo(Enum):
    SUCCESS = (1000, '成功')
    WEB_ELEMENT_NOT_FOUND = (10001, 'no web elements found!')
    EXCEPTION_OCCURRED = (99999, 'exception, reason is:')
