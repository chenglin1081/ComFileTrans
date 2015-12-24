# -*- coding: utf-8 -*-

from .singleton import Singleton
import os


class Environment(metaclass=Singleton):
    def __init__(self):
        self.app_name = 'com_tf'
        self.root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        dic = self.load_config() or {}
        self.port = int(dic.get('COM_PORT', 0))
        self.rate = int(dic.get('BAUD_RATE', 921600))
        self.side = int(dic.get('SIDE', 0)) << 7
        self.send_path = dic.get('SEND_PATH', r'c:\togeek\com\send')
        self.receive_path = dic.get('RECEIVE_PATH', r'c:\togeek\com\receive')
        self.log_path = dic.get('LOG_PATH', r'c:\togeek\com\log')

    def load_config(self):
        config_file = os.path.join(self.root, 'config.ini')
        if os.path.exists(config_file):
            with open(config_file) as f:
                lines = [(w[0].strip(), w[1].strip())
                         for w in [tuple(line.split('#')[0].split('=')) for line in f.readlines()]
                         if len(w) == 2]
                return {line[0]: line[1] for line in lines if all(line)}
