# -*- coding: utf-8 -*-

from random import randint
from time import time
from threading import RLock
from .session import Session
from ..lib.env import Environment
from ..lib.singleton import Singleton


class SessionPool(metaclass=Singleton):
    def __init__(self):
        self.env = Environment()
        self._pool = {}
        self.lock = RLock()
        self.onexists = self.onsuccess = None

    @property
    def values(self):
        return self._pool.values()

    def createSession(self, sid=None):
        if sid is None:
            while True:
                sid = randint(0, 127) | self.env.side
                if sid not in self._pool:
                    break
        session = Session(sid)
        self._pool[sid] = session
        return session

    def __getitem__(self, item):
        return self._pool.get(item)

    def delSession(self, sid):
        with self.lock:
            if sid in self._pool:
                self._pool[sid].close()
                del self._pool[sid]

    def delTimeoutSession(self):
        now = time()
        ls = [session.sid for session in self._pool.values() if now > session.overtime]
        for sid in ls:
            self.delSession(sid)

    def setAllTimeout(self):
        for session in self._pool.values():
            session.settimeout()

    def clear(self):
        for sid in self._pool:
            self.delSession(sid)
