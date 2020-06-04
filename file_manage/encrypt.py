def en(data):
    n = len(data)
    b = bytearray(n)
    for i in range(0, n):
        b[i] = data[i] + 1
    return bytes(b)


def de(data):
    n = len(data)
    b = bytearray(n)
    for i in range(0, n):
        b[i] = data[i] - 1
    return bytes(b)


def en2(sk, data):
    n = len(data)
    b = bytearray(n)
    for i in range(0, n):
        b[i] = (data[i] ^ sk) + 1
    return bytes(b)


def de2(sk, data):
    n = len(data)
    b = bytearray(n)
    for i in range(0, n):
        b[i] = (data[i] - 1) ^ sk
    return bytes(b)
