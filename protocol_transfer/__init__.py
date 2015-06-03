# -*- coding: utf-8 -*-

from .service import g
from .com import registerDevice
from .streamhelper import i2s, s2i, wrap, getdata
from .sender import Sender
from .receiver import Receiver
from .log import getLogger, log


def init():
    g.sender.start()
    g.receiver.start()


def close():
    g.receiver.close()
    g.sender.close()
    g.device.close()