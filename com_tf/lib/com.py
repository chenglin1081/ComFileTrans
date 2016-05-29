# -*- coding: utf-8 -*-

from serial import Serial
from threading import RLock
from time import sleep
from .singleton import Singleton
from .env import Environment
from .log import Log


class Com(metaclass=Singleton):
    def __init__(self, timeout=5):
        self.env = Environment()
        self.logger = Log().logger
        self.timeout = timeout
        self.com = Serial(port='COM' + str(self.env.port), baudrate=self.env.rate, timeout=self.timeout)
        self.logger.info('create device and open it')
        self.read_lock = RLock()
        self.write_lock = RLock()
        self.lock = RLock()

    def open(self):
        with self.lock:
            try:
                if not self.isOpen():
                    self.com.open()
                    self.logger.info('open device')
                return True
            except:
                self.close()
                self.logger.error('open device error')
                return False

    def close(self):
        with self.lock:
            self.com.close()
        self.logger.warning('device closed')
        sleep(1)

    def isOpen(self):
        return bool(self.com) and self.com.isOpen()

    def receiveSize(self):
        return self.com.inWaiting() if self.open() else 0

    def read(self, size=1):
        self.logger.debug('device reading')
        if size <= 0:
            return ''
        with self.read_lock:
            try:
                return self.com.read(size) if self.open() else ''
            except:
                self.close()
                self.logger.error('device read error')
                return ''

    def write(self, stream):
        self.logger.debug('device writing [%s] bytes' % len(stream))
        with self.write_lock:
            try:
                return self.com.write(stream) if self.open() else 0
            except:
                self.close()
                self.logger.error('device write error')
                return 0
