# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import logging.config

from value import LOGGING_CONFIG

#日志配置
logging.config.dictConfig(LOGGING_CONFIG)
logger=logging.getLogger('simple')