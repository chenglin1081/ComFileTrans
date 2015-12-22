# -*- coding: utf-8 -*-

import win32serviceutil
import win32service
import win32event
import traceback
from client import initialize, close, transfer_files, getLogger


class TranFileService(win32serviceutil.ServiceFramework):
    """传送文件的windows服务类"""
    _svc_name_ = 'TranFileService'
    _svc_display_name_ = 'TranFileService'
    _svc_description_ = '通过串口实时传输文件'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        getLogger().info('Service Init')

    def SvcStop(self):
        close()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        getLogger().info('Service Stoped')

    def SvcDoRun(self):
        self.timeout = 1000
        try:
            initialize()
        except:
            getLogger().error('Service Error:\n%s' % traceback.format_exc())
        while True:
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            if rc == win32event.WAIT_OBJECT_0:
                break
            else:
                try:
                    transfer_files()
                except Exception as ex:
                    getLogger().error('Service Error:\n%s' % traceback.format_exc())
                finally:
                    pass


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(TranFileService)
