import json
import os
import traceback as tb
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


def add_to_16(par):
    while len(par) % 16 != 0:  # 对字节型数据进行长度判断
        par += b'\x00'  # 如果字节型数据长度不是16倍整数就进行 补充
    return par


# def encrypt(sk, data):
#     b = bytearray(str(data).encode())
#     n = len(b)  # 计算字节数
#     c = bytearray(n * 2)
#     j = 0
#     for i in range(0, n):
#         b1 = b[i] ^ sk
#         c1 = b1 % 16 + 65
#         c2 = b1 // 16 + 65  # c1,c2都是0~15之间的数,加上65就变成了A-P 的字符的编码
#         c[j] = c1
#         c[j + 1] = c2
#         j = j + 2
#     return c.decode()
#
#
# def decrypt(sk, data):
#     try:
#         c = bytearray(str(data).encode())
#         n = len(c)  # 计算字节数
#         if n % 2 != 0:
#             return ""
#         n = n // 2
#         b = bytearray(n)
#         j = 0
#         for i in range(0, n):
#             c1 = c[j] - 65
#             c2 = c[j + 1] - 65
#             b1 = (c2 * 16 + c1) ^ sk
#             b[i] = b1
#             j = j + 2
#         return b.decode()
#     except Exception:
#         tb.print_exc()
#         log.error("解密失败")

# if __name__ == '__main__':
#     sk = 12
#     s1 = encrypt(sk, 'hello python')
#     s2 = decrypt(sk, s1)
#     print(s1, s2)

# 安装pycryptodome： pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pycryptodome
