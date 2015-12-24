# -*- coding: utf-8 -*-

from .streamhelper import *
from .sessionpool import SessionPool
from .command import SSN
from ..lib.log import Log


def process(stream):
    Log().logger.debug('process stream [%s] bytes' % len(stream))
    pool = SessionPool()
    sid = getsid(stream)
    session = pool[sid]
    if not session:
        command = getcommand(stream)
        if command == SSN:
            session = pool.createSession(sid)
    if session:
        session.process(stream)
    pool.delTimeoutSession()


def clear():
    SessionPool().clear()
