# -*- coding: utf-8 -*-

import protocol_transfer as pt
from protocol_transfer import i2s, s2i


def wrap(sid, command, *data):
    return pt.wrap(i2s(sid), i2s(command), *data)


def getsid(stream):
    return stream[4]


def getcommand(stream):
    return stream[5]


DATASTARTPOINT = 6
FILESIZEBYTE = 6
FILEBLOCKNUMBYTE = 4
