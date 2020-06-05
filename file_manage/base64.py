import math

BASEDATA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'


# 补齐到6位_在后面补充
def add_to_6s(data):
    if len(data) % 6 != 0:
        data = data + "0" * (6 - len(data) % 6)
    else:
        pass
    return data


# 补齐到6位_在前面补充
def add_to_6p(data):
    if len(data) % 6 != 0:
        data = "0" * (6 - len(data) % 6) + data
    else:
        pass
    return data


def encode_base64(data):
    bin_str = ""
    # 将所有字符转为2进制
    for letter in data:
        if letter == " ":
            bin_str += bin(ord(letter)).replace("b", "0")
        else:
            bin_str += bin(ord(letter)).replace("b", "")
    # 计算可拆分的组数
    count = int(math.ceil(len(bin_str) / 24))
    all_str = ""
    for i in range(count):
        bin24 = bin_str[i * 24:(i + 1) * 24]  # 每24位一组

        if len(bin24) % 6 != 0:
            bin24 = add_to_6s(bin24)  # 不足24位，补充成6的倍数

        for j in range(int(len(bin24) / 6)):
            index = int(bin24[j * 6:(j + 1) * 6], 2)  # 每6位一组，并转为10进制数
            all_str += BASEDATA[index]  # 对照base64索引表获取转换后字符

        if len(all_str) % 4 != 0:
            all_str += "=" * (4 - len(all_str) % 4)  # 如果最终字符不是4的整数倍，用=号填充
    return all_str


def decode_base64(data):
    origin = data.replace("=", "")  # 去除补充的=号
    bin_all = ""
    for letter in origin:
        index = BASEDATA.index(letter)  # 根据base64索引表取出对应数字
        bin_all += add_to_6p(bin(index).replace("0b", ""))  # 数字换成6位的二进制数
    remain = len(bin_all) % 8
    if remain != 0:
        bin_all = bin_all[0: - remain]  # 去除补充的0

    all_str = ""
    for i in range(int(len(bin_all) / 8)):
        bin8 = bin_all[i * 8:(i + 1) * 8]  # 获取8位二进制数
        oc = int(bin8, 2)  # 换成十进制
        all_str += chr(oc)  # 换成ASCIII字符并累加
    return all_str


if __name__ == '__main__':
    data = 'hello python\n'
    s1 = encode_base64(data)
    s2 = decode_base64(s1)
    print(s1, s2)
