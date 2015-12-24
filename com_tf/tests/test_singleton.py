# -*- coding: utf-8 -*-

from com_tf.lib.singleton import Singleton


class A:
    def __init__(self):
        print('A init')


class B(A, metaclass=Singleton):
    def __init__(self):
        super(B, self).__init__()
        print('B init')


if __name__ == '__main__':
    o1 = B()
    o2 = B()
    assert o1 is o2
