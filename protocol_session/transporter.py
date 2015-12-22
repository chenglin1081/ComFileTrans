# -*- coding: utf-8 -*-

import os
from protocol_transfer import g


def transfer(fullname):
    fullname = os.path.abspath(fullname)
    filename = os.path.basename(fullname)
    sending = [os.path.basename(n).lower() for n in getoutfiles()]
    if filename.lower() in sending:
        return
    session = g.sessionpool.createSession()
    session.transferfile(fullname)
    return session


def getoutfiles():
    g.sessionpool.delTimeoutSession()
    return [session.fullname for session in g.sessionpool.values if session.issender]


def getinfiles():
    g.sessionpool.delTimeoutSession()
    return [session.fullname for session in g.sessionpool.values if not session.issender]
