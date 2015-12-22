# -*- coding: utf-8 -*-

from .streamhelper import *
from protocol_transfer import g, log

SSN = 0x01
ASN = 0x02
TFI = 0x04
EXF = 0x07
RFB = 0x08
TFB = 0x09
FFL = 0x0C
SFF = 0x0D
FFF = 0x0E


@log
def processSSN(session, stream):
    """
    收到启动会话指令，返回确认启动会话指令
    """
    return wrap(session.sid, ASN)


@log
def processASN(session, stream):
    """
    收到会话启动确认指令，开始发送文件信息
    """
    return wrap(session.sid, TFI, i2s(session.fullsize, FILESIZEBYTE), session.filename.encode())


@log
def processTFI(session, stream):
    """
    收到传送文件信息指令，保存文件信息，确认文件信息
    """
    if session.receivefile(stream[DATASTARTPOINT + FILESIZEBYTE:].decode(),
                           s2i(stream[DATASTARTPOINT:DATASTARTPOINT + FILESIZEBYTE])):
        return wrap(session.sid, RFB, i2s(session.tmpnextblock, FILEBLOCKNUMBYTE))
    else:
        return wrap(session.sid, EXF)


@log
def processEXF(session, stream):
    """
    收到文件存在指令
    """
    session.settimeout()
    g.sessionpool.onexists(session)


@log
def processRFB(session, stream):
    """
    收到请求发送文件块
    """
    blocknum = s2i(stream[DATASTARTPOINT:DATASTARTPOINT + FILEBLOCKNUMBYTE])
    data = session.readblock(blocknum)
    if data:
        return wrap(session.sid, TFB, i2s(blocknum, FILEBLOCKNUMBYTE), data)
    return wrap(session.sid, FFL)


@log
def processTFB(session, stream):
    """
    收到文件块
    """
    num = s2i(stream[DATASTARTPOINT:DATASTARTPOINT + FILEBLOCKNUMBYTE])
    data = stream[DATASTARTPOINT + FILEBLOCKNUMBYTE:]
    if session.writeblock(num, data):
        return wrap(session.sid, RFB, i2s(num + 1, FILEBLOCKNUMBYTE))
    else:
        return wrap(session.sid, RFB, i2s(session.tmpnextblock, FILEBLOCKNUMBYTE))


@log
def processFFL(session, stream):
    """
    收到结束文件传输
    """
    if session.completereceive():
        g.sessionpool.onsuccess(session)
        return wrap(session.sid, SFF)
    return wrap(session.sid, FFF)


@log
def processSFF(session, stream):
    """
    收到文件正确接收指令
    """
    session.close()
    g.sessionpool.onsuccess(session)


@log
def processFFF(session, stream):
    """
    收到文件接收错误指令
    """
    session.close()


@log
def processECR(session, stream):
    """
    收到CRC校验错误指令，则重新发送会话缓存字符串流
    """
    g.sessionpool.occurCrcErr()
    return session.cache


cfmap = {}
cfmap[SSN] = (processSSN, 'receive start session command')
cfmap[ASN] = (processASN, 'remote session created')
cfmap[TFI] = (processTFI, 'get file info')
cfmap[EXF] = (processEXF, 'remote file exists')
cfmap[RFB] = (processRFB, 'remote want file block')
cfmap[TFB] = (processTFB, 'get file block')
cfmap[FFL] = (processFFL, 'remote transfer end')
cfmap[SFF] = (processSFF, 'remote receive file success')
cfmap[FFF] = (processFFF, 'remote receive file failed')
