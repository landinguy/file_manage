import json
import os
import uuid

import logger
from file_manage import db
from file_manage.entity import File

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


def add_to_16(par):
    while len(par) % 16 != 0:  # 对字节型数据进行长度判断
        par += b'\x00'  # 如果字节型数据长度不是16倍整数就进行 补充
    return par


if __name__ == '__main__':
    print()
    # with open('D:/aa.txt', 'rb') as f:
    #     content = f.read()
    #     print(content)
    #     with open('D:/bb.fm', 'wb') as f2:
    #         encode = base64.b64encode(content)
    #         print('encode', encode)
    #         f2.write(encode)

    # with open('D:/bb.fm', 'rb') as f:
    #     read = f.read()
    #     print(read)
    #     with open('D:/cc.txt', 'wb') as f2:
    #         decode = base64.b64decode(read)
    #         print('decode', decode)
    #         f2.write(decode)

    # password = '123456'.encode()
    # text = 'hello world'.encode()
    # model = AES.MODE_ECB  # 定义模式
    # aes = AES.new(add_to_16(password), model)  # 创建一个aes对象
    #
    # en_text = aes.encrypt(add_to_16(text))  # 加密明文
    # print(en_text)
    #
    # decrypt = aes.decrypt(en_text)
    # print(decrypt)
    list = db.get_session().query(File).all()

    print([x.__dict__ for x in list])
# 安装pycryptodome： pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pycryptodome
