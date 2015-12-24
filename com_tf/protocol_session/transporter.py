# -*- coding: utf-8 -*-

import os
from .sessionpool import SessionPool


def transfer(fullname):
    fullname = os.path.abspath(fullname)
    filename = os.path.basename(fullname)
    sending = [os.path.basename(n).lower() for n in getoutfiles()]
    if filename.lower() in sending:
        return
    session = SessionPool().createSession()
    session.transferfile(fullname)
    return session


def getoutfiles():
    pool = SessionPool()
    pool.delTimeoutSession()
    return [session.fullname for session in pool.values if session.issender]


def getinfiles():
    pool = SessionPool()
    pool.delTimeoutSession()
    return [session.fullname for session in pool.values if not session.issender]
