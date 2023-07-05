import shutil
import numpy as np
import struct
from collections import defaultdict

def encoding(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        s1 = f.read()
    table = defaultdict(int)
    for i in range(256):
        ch = chr(i)
        table[ch] = i

    p = s1[0]
    code = 256
    output_code = []
    for i in range(len(s1)):
        if i != len(s1) - 1:
            c = s1[i + 1]
        if p + c in table:
            p = p + c
        else:
            output_code.append(table[p])
            table[p + c] = code
            code += 1
            p = c
        c = ""
    output_code.append(table[p])
    return output_code

def decoding(op, file_path):
    table = defaultdict(str)
    for i in range(256):
        ch = chr(i)
        table[i] = ch
    old = op[0]
    s = table[old]
    c = s[0]
    count = 256
    with open(file_path, 'w') as f:
        f.write(s)
        for i in range(len(op) - 1):
            n = op[i + 1]
            if n not in table:
                s = table[old]
                s += c
            else:
                s = table[n]
            f.write(s)
            c = s[0]
            table[count] = table[old] + c
            count += 1
            old = n

def save_binary_file(data, file_path):
    with open(file_path, 'wb') as f:
        f.write(struct.pack(f'{len(data)}I', *data))


def load_binary_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    return list(struct.unpack(f'{len(data)//4}I', data))

def encoding_inputtext(text):
    s1 = text
    table = defaultdict(int)
    for i in range(256):
        ch = chr(i)
        table[ch] = i

    p = s1[0]
    code = 256
    dict_arr = []
    output_code = []
    for i in range(len(s1)):
        if i != len(s1) - 1:
            c = s1[i + 1]
        if p + c in table:
            p = p + c
            # print(p, table[p])
        else:
            dict_arr.append([p,table[p]])
            output_code.append(table[p])
            table[p + c] = code
            code += 1
            p = c
        c = ""
    dict_arr.append([p,table[p]])
    output_code.append(table[p])

    # print('Table', table)
    return dict_arr, output_code

def decoding_inputtext(op):
    table = defaultdict(str)
    for i in range(256):
        ch = chr(i)
        table[i] = ch
    old = op[0]
    s = table[old]
    c = s[0]
    count = 256
    temp = ''
    temp += s
    for i in range(len(op) - 1):
        n = op[i + 1]
        if n not in table:
            s = table[old]
            s += c
        else:
            s = table[n]
        temp += s
        c = s[0]
        table[count] = table[old] + c
        count += 1
        old = n
    return temp