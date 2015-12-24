# -*- coding: utf-8 -*-

from com_tf.lib.env import Environment


def test():
    env = Environment()
    print(env.app_name)
    print(env.root)
    print(env.port)
    print(env.rate)
    print(env.side)
    print(env.send_path)
    print(env.receive_path)
    print(env.log_path)


if __name__ == '__main__':
    test()
