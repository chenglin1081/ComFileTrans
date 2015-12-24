# -*- coding: utf-8 -*-

import os
import traceback
from time import time
from .command import *
from .fileprocess import FileReader, FileWriter
from ..lib.env import Environment
from ..lib.log import Log
from ..protocol_transfer import Sender


class Session:
    BLOCK = 4000
    TIMEOUT = 10

    def __init__(self, sid):
        from ..protocol_session import SessionPool
        self.env = Environment()
        self.sessionpool = SessionPool()
        self.sender = Sender()
        self.logger = Log().logger
        self.resetovertime()
        self.sid = sid
        self.fileproc = None
        self.fullname = None
        self.filename = None
        self.fullsize = None
        self.logger.info('[%s] session created' % self.sid)

    @property
    def tmpname(self):
        return self.fullname + '.tmp'

    @property
    def tmpnextblock(self):
        return int(len(self.fileproc) / Session.BLOCK)

    @property
    def issender(self):
        return not (self.sid >> 7) ^ (self.env.side >> 7)

    def resetovertime(self):
        self.overtime = time() + Session.TIMEOUT

    def settimeout(self):
        self.overtime = 0

    def transferfile(self, fullname):
        self.fullname = fullname
        self.filename = os.path.basename(fullname)
        self.fileproc = FileReader(fullname)
        self.fullsize = len(self.fileproc)
        self.sender.send(wrap(self.sid, SSN))
        self.logger.info('[%s] begin send file [%s]' % (self.sid, fullname))

    def receivefile(self, filename, size):
        self.filename = filename
        self.fullname = os.path.join(self.env.receive_path, self.filename)
        self.fullsize = size
        if os.path.exists(self.fullname):
            self.close()
            self.sessionpool.onexists(self)
            return False
        self.fileproc = FileWriter(self.tmpname)
        return True

    def writeblock(self, blocknum, data):
        if not data or self.tmpnextblock < blocknum:
            return False
        sp = blocknum * Session.BLOCK
        if len(self.fileproc) != sp:
            self.fileproc.truncate(sp)
        self.fileproc.write(data)
        return True

    def readblock(self, blocknum):
        self.logger.debug('[%s] Read file block [#%s]' % (self.sid, blocknum))
        return self.fileproc.read(blocknum * Session.BLOCK, Session.BLOCK)

    def completereceive(self):
        if len(self.fileproc) == self.fullsize:
            self.close()
            os.rename(self.tmpname, self.fullname)
            return True
        else:
            self.close()
            self.logger.error('[%s] Receive file length error' % self.sid)
            os.remove(self.tmpname)
            return False

    def process(self, stream):
        command = getcommand(stream)
        func, desc = cfmap.get(command, (None, None))
        if func:
            self.resetovertime()
            try:
                data = func(self, stream)
                if isinstance(data, bytes) and len(data) >= DATASTARTPOINT:
                    self.logger.debug('[%s] Process[%s] write %d bytes' % (self.sid, desc, len(data)))
                    self.sender.send(data)
            except:
                self.logger.error(traceback.format_exc())
                self.close()
        else:
            self.logger.error('Unknow command code [%s]' % command)
            self.close()

    def close(self):
        if self.fileproc:
            self.fileproc.close()
            self.fileproc = None
        self.settimeout()
        self.logger.info('[%s] session closed' % self.sid)
