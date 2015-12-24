# -*- coding: utf-8 -*-

import os
import sys
import logging
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
from .singleton import Singleton
from .env import Environment


class Log(metaclass=Singleton):
    def __init__(self, level=logging.INFO, print_std=True):
        self.env = Environment()
        self._logger = logging.getLogger(self.env.app_name)
        self._logger.setLevel(level)
        self._logger.handlers.clear()
        log_format_str = '%(asctime)s\n[%(levelname)s][%(module)s]' \
                         '[PID: %(process)d][TID: %(thread)d %(threadName)s] - %(message)s'
        log_format = logging.Formatter(log_format_str)
        if self.env.log_path:
            self.file = os.path.join(self.env.log_path, 'log.txt')
            if not os.path.exists(self.env.log_path):
                os.mkdir(self.env.log_path)
            log_handler = TimedRotatingFileHandler(self.file, when='h', interval=1, backupCount=24)
            log_handler.setFormatter(log_format)
            self._logger.addHandler(log_handler)

        if print_std:
            log_handler = StreamHandler(sys.stdout)
            log_handler.setFormatter(log_format)
            self._logger.addHandler(log_handler)

    @property
    def logger(self):
        return self._logger


def log(func):
    def __inner__(*args, **kwargs):
        Log().logger.debug('call function [%s]' % func)
        return func(*args, **kwargs)

    return __inner__
