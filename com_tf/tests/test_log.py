# -*- coding: utf-8 -*-

from com_tf.lib.log import Log


def test():
    log = Log(print_std=True)
    log.logger.info('this is a test!')


if __name__ == '__main__':
    test()
