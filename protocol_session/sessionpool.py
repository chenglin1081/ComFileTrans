# -*- coding: utf-8 -*-

import os
from random import randint
from time import time
from protocol_transfer import g
from threading import RLock
from .session import Session


class SessionPool(object):
    _pool = {}
    lock = RLock()
    side, targetpath, onexists, onsuccess = 0, None, None, None

    @property
    def values(self):
        return self._pool.values()

    def createSession(self, sid=None):
        if sid == None:
            while True:
                sid = randint(0, 127) | self.side
                if sid not in self._pool.keys():
                    break
        session = Session(sid)
        self._pool[sid] = session
        return session

    def __getitem__(self, item):
        return self._pool.get(item)

    def delSession(self, sid):
        with SessionPool.lock:
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
        for sid in self._pool.keys():
            self.delSession(sid)


def registerSessionPool(side, targetpath, onexists, onsuccess):
    def wrap(func):
        def _inner(pool, *args, **kwargs):
            return func(*args, **kwargs)

        return _inner

    if not g.get('sessionpool'):
        if side in [0, 1]:
            SessionPool.side = side << 7
        else:
            raise Exception('Side not is 0 or 1')
        if not os.path.exists(targetpath):
            os.mkdir(targetpath)
        SessionPool.targetpath = targetpath
        SessionPool.onexists = wrap(onexists)
        SessionPool.onsuccess = wrap(onsuccess)
        g.set('sessionpool', SessionPool())