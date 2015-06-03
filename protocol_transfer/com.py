# -*- coding: utf-8 -*-

from serial import Serial
from threading import RLock
from time import sleep
from .service import g
from .log import getLogger


class Com(object):
    readlock = RLock()
    writelock = RLock()
    lock = RLock()

    def __init__(self, port, baudrate, timeout=5):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.com = None

    def open(self):
        with Com.lock:
            try:
                if not self.com:
                    self.com = Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
                    getLogger().info('create device and open it')
                if not self.isOpen():
                    self.com.open()
                    getLogger().info('open device')
                return True
            except:
                self.close()
                getLogger().error('open device error')
                return False

    def close(self):
        if self.com:
            with Com.lock:
                self.com.close()
            getLogger().warning('device closed')
            sleep(1)

    def isOpen(self):
        return bool(self.com) and self.com.isOpen()

    def receiveSize(self):
        return self.com.inWaiting() if self.open() else 0

    def read(self, size=1):
        getLogger().debug('device reading')
        if size <= 0:
            return ''
        with Com.readlock:
            try:
                return self.com.read(size) if self.open() else ''
            except:
                self.close()
                getLogger().error('device read error')
                return ''

    def write(self, stream):
        getLogger().debug('device writing [%s] bytes' % len(stream))
        with Com.writelock:
            try:
                return self.com.write(stream) if self.open() else 0
            except:
                self.close()
                getLogger().error('device write error')
                return 0


def registerDevice(port, baudrate, timeout=2):
    if not g.get('device'):
        g.set('device', Com(port, baudrate, timeout))
        g.device.open()