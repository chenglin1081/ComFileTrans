# -*- coding: utf-8 -*-

from binascii import crc_hqx


def crc(stream):
    return crc_hqx(stream, 0)


def i2s(num, length=0):
    ns = []
    while True:
        ns.append(num & 0xff)
        num = num >> 8
        if not num:
            break
    return bytes(ns).ljust(length, b'\x00')


def s2i(stream):
    num = 0
    for i in range(len(stream)):
        num |= stream[i] << i * 8
    return num


def wrap(*data):
    s = b''.join(data)
    length = len(s) + 4
    return i2s(length, 2) + i2s(crc(s), 2) + s


def checkcrc(stream):
    return s2i(stream[2:4]) == crc(getdata(stream))


def getlength(stream):
    return s2i(stream[:2])


def getdata(stream):
    return stream[4:]


TICK = i2s(10000, 2)
ERROR = i2s(10001, 2)

if __name__ == '__main__':
    stream = b'jiangce'
    ws = wrap(stream)
    assert getlength(ws) == len(ws)
    assert checkcrc(ws)