# -*- coding: utf-8 -*-

from threading import Thread
from .service import g
from .streamhelper import TICK, ERROR, s2i, checkcrc
from .log import getLogger


class Receiver(Thread):
    def __init__(self):
        super(Receiver, self).__init__()
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
            head = g.device.read(2)
            if not self._running:
                return
            if not head:
                continue
            if len(head) != 2:
                getLogger().error('device read head error')
                self.clear()
            else:
                length = s2i(head)
                if length == 10000:
                    getLogger().debug('get a TICK')
                    g.sender.cansend = True
                elif length < 5 or length > 10000:
                    getLogger().error('device read error')
                    self.clear()
                else:
                    stream = head + g.device.read(length - 2)
                    if not self._running:
                        return
                    getLogger().debug('device get [%s] bytes' % len(stream))
                    if length == len(stream):
                        if checkcrc(stream):
                            getLogger().debug('device send TICK')
                            g.device.write(TICK)
                            if self.callback:
                                self.callback(stream)
                        else:
                            getLogger().error('device read crc error')
                            self.clear()
                    else:
                        getLogger().error('length error: head[%s] <> receive[%s]' % (length, len(stream)))
                        self.clear()

    def clear(self):
        g.device.write(ERROR)
        g.device.close()
        if self.errcallback:
            self.errcallback()

    def close(self):
        self._running = False

    def run(self):
        self.loop()


g.set('receiver', Receiver())