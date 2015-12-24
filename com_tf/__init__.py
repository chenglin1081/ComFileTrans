# -*- coding: utf-8 -*-

import sys
import time
import traceback
import logging
from .lib.env import Environment
from .lib.log import Log
from .client import initialize, close, transfer_files

version = '1.0.1'
env = Environment()
log = Log(level=logging.INFO, print_std='--print' in [a.lower() for a in sys.argv])


def main():
    while True:
        try:
            initialize()
        except:
            close()
            log.logger.error('Init error:\n%s' % traceback.format_exc())
            return
        while True:
            try:
                time.sleep(1)
                transfer_files()
            except:
                close()
                log.logger.error('Trans file error:\n%s' % traceback.format_exc())
                break
