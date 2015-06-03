# -*- coding: utf-8 -*-

from .streamhelper import *
from .command import SSN
from protocol_transfer import g, getLogger


def process(stream):
    getLogger().debug('process stream [%s] bytes' % len(stream))
    sid = getsid(stream)
    session = g.sessionpool[sid]
    if not session:
        command = getcommand(stream)
        if command == SSN:
            session = g.sessionpool.createSession(sid)
    if session:
        session.process(stream)
    g.sessionpool.delTimeoutSession()


def clear():
    g.sessionpool.clear()


g.receiver.registerCallback(process, clear)