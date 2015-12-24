# -*- coding: utf-8 -*-

from .streamhelper import i2s, s2i, wrap, getdata
from .sender import Sender
from .receiver import Receiver
from ..lib.com import Com


def init():
    Com().open()
    Sender().start()
    Receiver().start()


def close():
    Receiver().close()
    Sender().close()
    Com().close()
