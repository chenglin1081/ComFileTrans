# -*- coding: utf-8 -*-

import os, logging
from logging.handlers import TimedRotatingFileHandler

LOG_NAME = 'comtrans'
LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'log'))
LOG_FILE = os.path.join(LOG_PATH, 'log.txt')


def getLogger():
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)
    logger = logging.getLogger(LOG_NAME)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        log_handler = TimedRotatingFileHandler(LOG_FILE, when='d', interval=1, backupCount=7)
        log_formater_str = '%(asctime)s\n[%(levelname)s][%(module)s]' \
                           '[PID: %(process)d][TID: %(thread)d %(threadName)s] - %(message)s'
        log_formater = logging.Formatter(log_formater_str)
        log_handler.setFormatter(log_formater)
        logger.addHandler(log_handler)
    return logger


def log(func):
    def __inner__(*args, **kwargs):
        getLogger().debug('call function [%s]' % func)
        return func(*args, **kwargs)

    return __inner__