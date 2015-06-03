# -*- coding: utf-8 -*-

from protocol_transfer import g, registerDevice, getLogger, log, init as _init, close as _close
from .streamprocess import process, clear
from .transporter import transfer, getoutfiles, getinfiles
from .sessionpool import registerSessionPool


def init():
    _init()


def close():
    _close()
    g.sessionpool.clear()