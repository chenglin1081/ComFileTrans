# -*- coding: utf-8 -*-

from threading import Thread
from queue import Queue
from collections import deque
from time import time
from .service import g
from .log import getLogger


class Sender(Thread):
    EXIT = 0

    def __init__(self):
        super(Sender, self).__init__()
        self.name = 'com_send'
        self.setDaemon(False)
        self.data = None
        self.que = deque()
        self.channel = Queue()
        self._cansend = True
        self.sendtime = time()

    @property
    def cansend(self):
        return self._cansend and self.data and g.device.open()

    @cansend.setter
    def cansend(self, value):
        getLogger().debug('set cansend = %s' % value)
        self._cansend = value
        self.send(True)

    def send(self, obj):
        self.channel.put(obj)

    def loop(self):
        while True:
            obj = self.channel.get()
            if obj == Sender.EXIT:
                getLogger().info('remove sender thread')
                return
            if time() - self.sendtime > g.device.timeout:
                self._cansend = True
            if isinstance(obj, bytes):
                self.que.append(obj)
                getLogger().debug('sender channel get [%s] bytes' % len(obj))
            self.data = self.data or (self.que.popleft() if self.que else None)
            if self.cansend:
                if g.device.write(self.data) == 0:
                    self.clear()
                self._cansend = False
                self.data = None
                self.sendtime = time()

    def clear(self):
        self.data = None
        self.que.clear()
        g.device.close()
        self._cansend = True
        self.sendtime = time()

    def close(self):
        self.send(Sender.EXIT)

    def run(self):
        self.loop()


g.set('sender', Sender())
