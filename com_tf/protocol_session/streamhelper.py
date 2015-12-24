# -*- coding: utf-8 -*-

from ..protocol_transfer import i2s, wrap as pt_wrap


def wrap(sid, command, *data):
    return pt_wrap(i2s(sid), i2s(command), *data)


def getsid(stream):
    return stream[4]


def getcommand(stream):
    return stream[5]


DATASTARTPOINT = 6
FILESIZEBYTE = 6
FILEBLOCKNUMBYTE = 4
