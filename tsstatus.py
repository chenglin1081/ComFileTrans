# -*- coding: utf-8 -*-

from tranfileservice import TranFileService
import win32serviceutil
import os
import time


def getServiceStatus():
   '''
   return a tuple (flag1, flag2)
   flag1: whether the service is installed
   flag2: whether the service is running
   '''
   SERVICE_RUNNING = 0x4
   try:
      status = win32serviceutil.QueryServiceStatus(
         TranFileService._svc_name_)
      return (True, status[1] == SERVICE_RUNNING)
   except:
      return (False, False)

def installService():
   if getServiceStatus()[0]:
      return True
   os.system('tranfileservice.py --startup auto install')
   return getServiceStatus()[0]

def uninstallService():
   if not getServiceStatus()[0]:
      return True
   os.system('tranfileservice.py remove')
   return not getServiceStatus()[0]

def startService():
   if getServiceStatus()[1]:
      return True
   os.system('tranfileservice.py start')
   time.sleep(1)
   return getServiceStatus()[1]

def stopService():
   if not getServiceStatus()[1]:
      return True
   os.system('tranfileservice.py stop')
   return not getServiceStatus()[1]

def startService2():
   if getServiceStatus()[1]:
      return True
   os.system('sc start TranFileService')
   time.sleep(1)
   return getServiceStatus()[1]

def stopService2():
   if not getServiceStatus()[1]:
      return True
   os.system('sc stop TranFileService')
   time.sleep(1)
   return getServiceStatus()[1]
