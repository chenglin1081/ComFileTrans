# -*- coding: utf-8 -*-

import sys
import getopt
import os

_help = '''
tranfileservice.py服务的控制，相关参数：
-h  帮助
-i  安装服务
-u  更新服务
-r  移除服务
-b  启动服务
-e  停止服务
'''

if __name__ == '__main__':
   option, args = getopt.getopt(sys.argv[1:], 'hiurbe')
   if not len(option) or len(option) > 1:
      print('请仅仅指定一个选项,-h获取帮助')
      sys.exit(1)
   for o, a in option:
      if o == '-h':
         print(_help)
      elif o == '-i':
         os.system('tranfileservice.py --startup auto install')
      elif o == '-b':
         os.system('tranfileservice.py start')
      elif o == '-e':
         os.system('tranfileservice.py stop')
      elif o == '-r':
         os.system('tranfileservice.py remove')
      elif o == '-u':
         os.system('tranfileservice.py update')
