import json
import os
import uuid

import logger

log = logger.get()


class Result(object):
    def __init__(self, code=0, msg='success', data=None):
        self.code = code
        self.msg = msg
        self.data = data


def dump(obj) -> str: return json.dumps(obj.__dict__, ensure_ascii=False)


def get_uuid() -> str: return str(uuid.uuid1()).replace('-', '')


def remove(path):
    os.remove(path)


def make_file(n=1):
    size = n * 1024 * 1024
    text = 'stay foolish,stay hungry!哈哈\n'
    path = 'd:/text-{0}m.txt'.format(n)
    with open(path, 'w') as f:
        n = 1
        m = size // len(text)
        while n <= m:
            n += 1
            f.write(text)


if __name__ == '__main__':
    make_file(10)

# 安装pycryptodome： pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pycryptodome
