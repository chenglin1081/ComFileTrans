# -*- coding: utf-8 -*-

class Service(object):
    def __init__(self):
        self._service = {}

    def set(self, name, value):
        self.__dict__['_service'][name] = value

    def get(self, name):
        return self._service.get(name)

    def all(self):
        return self._service

    def __getattr__(self, name):
        return self._service[name]


g = Service()

if __name__ == '__main__':
    g.set('test', 'test')
    assert g.test == 'test'
