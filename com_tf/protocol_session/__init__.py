# -*- coding: utf-8 -*-

from ..protocol_transfer import init as _init, close as _close, Receiver
from .sessionpool import SessionPool
from .streamprocess import process, clear
from .transporter import transfer, getoutfiles, getinfiles


def init():
    Receiver().registerCallback(process, clear)
    _init()


def close():
    _close()
    SessionPool().clear()
