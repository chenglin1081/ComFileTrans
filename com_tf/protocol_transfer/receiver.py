# -*- coding: utf-8 -*-

from ..lib.singleton import Singleton
from ..lib.com import Com
from ..lib.log import Log
from .sender import Sender
from .streamhelper import TICK, ERROR, s2i, checkcrc
from threading import Thread


class Receiver(Thread, metaclass=Singleton):
    def __init__(self):
        super(Receiver, self).__init__()
        self.device = Com()
        self.sender = Sender()
        self.logger = Log().logger
        self.name = 'com_receiver'
        self.setDaemon(False)
        self._running = True
        self.callback = None
        self.errcallback = None

    def registerCallback(self, callback, errcallback):
        self.callback = callback
        self.errcallback = errcallback

    def loop(self):
        while self._running:
            head = self.device.read(2)
            if not self._running:
                return
            if not head:
                continue
            if len(head) != 2:
                self.logger.error('device read head error')
                self.clear()
            else:
                length = s2i(head)
                if length == 10000:
                    self.logger.debug('get a TICK')
                    self.sender.cansend = True
                elif length < 5 or length > 10000:
                    self.logger.error('device read error')
                    self.clear()
                else:
                    stream = head + self.device.read(length - 2)
                    if not self._running:
                        return
                    self.logger.debug('device get [%s] bytes' % len(stream))
                    if length == len(stream):
                        if checkcrc(stream):
                            self.logger.debug('device send TICK')
                            self.device.write(TICK)
                            if self.callback:
                                self.callback(stream)
                        else:
                            self.logger.error('device read crc error')
                            self.clear()
                    else:
                        self.logger.error('length error: head[%s] <> receive[%s]' % (length, len(stream)))
                        self.clear()

    def clear(self):
        self.device.write(ERROR)
        self.device.close()
        if self.errcallback:
            self.errcallback()

    def close(self):
        self._running = False

    def run(self):
        self.loop()
