# -*- coding: utf-8 -*-

from ..lib.singleton import Singleton
from ..lib.com import Com
from ..lib.log import Log
from threading import Thread
from queue import Queue
from collections import deque
from time import time


class Sender(Thread, metaclass=Singleton):
    def __init__(self):
        super(Sender, self).__init__()
        self.device = Com()
        self.logger = Log().logger
        self.EXIT = 0
        self.name = 'com_send'
        self.setDaemon(False)
        self.data = None
        self.que = deque()
        self.channel = Queue()
        self._cansend = True
        self.sendtime = time()

    @property
    def cansend(self):
        return self._cansend and self.data and self.device.open()

    @cansend.setter
    def cansend(self, value):
        self.logger.debug('set cansend = %s' % value)
        self._cansend = value
        self.send(True)

    def send(self, obj):
        self.channel.put(obj)

    def loop(self):
        while True:
            obj = self.channel.get()
            if obj == self.EXIT:
                self.logger.info('remove sender thread')
                return
            if time() - self.sendtime > self.device.timeout:
                self._cansend = True
            if isinstance(obj, bytes):
                self.que.append(obj)
                self.logger.debug('sender channel get [%s] bytes' % len(obj))
            self.data = self.data or (self.que.popleft() if self.que else None)
            if self.cansend:
                if self.device.write(self.data) == 0:
                    self.clear()
                self._cansend = False
                self.data = None
                self.sendtime = time()

    def clear(self):
        self.data = None
        self.que.clear()
        self.device.close()
        self._cansend = True
        self.sendtime = time()

    def close(self):
        self.send(self.EXIT)

    def run(self):
        self.loop()
