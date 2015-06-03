# -*- coding: utf-8 -*-

import os
from protocol_session import *

COM_PORT = 0
BAUD_RATE = 921600
SEND_PATH = r'c:\togeek\com\send'
RECEIVE_PATH = r'c:\togeek\com\receive'
SIDE = 0

PROG_PATH = os.path.dirname(__file__)


def read_config():
    try:
        with open(os.path.join(PROG_PATH, 'config.ini')) as f:
            exec(f.read())
    except:
        getLogger().error('Load config file error')


def onsuccess(session):
    getLogger().info('[%s] %s -> send success' % (session.sid, session.filename))
    if session.issender:
        os.remove(session.fullname)


def onexists(session):
    getLogger().info('[%s] %s -> file exists, delete it' % (session.sid, session.filename))
    if not session.issender:
        os.remove(session.fullname)


def initialize():
    read_config()
    registerDevice(COM_PORT, BAUD_RATE)
    registerSessionPool(SIDE, RECEIVE_PATH, onexists, onsuccess)
    g.set('run', True)
    init()


def transfer_files():
    if g.run:
        for name in os.listdir(SEND_PATH):
            if len(getoutfiles()) >= 3:
                break
            fullname = os.path.join(SEND_PATH, name)
            if not os.path.isfile(fullname) or name.lower().endswith('.tmp'):
                continue
            transfer(fullname)


def closeAll():
    g.set('run', False)
    close()


if __name__ == '__main__':
    from time import sleep
    initialize()
    for i in range(10):
        transfer_files()
        sleep(5)
    close()