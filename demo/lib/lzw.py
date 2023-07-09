import shutil
from collections import defaultdict
from PIL import Image
import numpy as np
import re
import sys
import struct

# Nén file text
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

#  Nén văn bản được nhập vào
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


#  Nén ảnh
def read_image_to_string(file_path):
    my_string = np.asarray(Image.open(file_path),np.uint8)
    sudhi = my_string
    shape = my_string.shape
    print ("Enetered string is:",my_string)
    stringToEncode = str(my_string.tolist())
    s1 = stringToEncode
    return s1, shape

def encoding_img(s1):
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
            #print(p, table[p])
            table[p + c] = code
            code += 1
            p = c
        c = ""
    output_code.append(table[p])
    #print(p, table[p])
    # print(output_code)
    #print(output_string)
    #print('encode: ',(len(s1) * 8 - len(output_string)*8)/(len(s1) * 8))
    input_size = len(s1)
    return output_code

def decoding_img(op,shape):
    table = defaultdict(str)
    for i in range(256):
        ch = chr(i)
        table[i] = ch
    old = op[0]
    s = table[old]
    c = s[0]
    count = 256
    # with open(file_path, 'w') as f:
    #     f.write(s)
    output = s
    for i in range(len(op) - 1):
        n = op[i + 1]
        if n not in table:
            s = table[old]
            s += c
        else:
            s = table[n]
        output += s
        c = s[0]
        table[count] = table[old] + c
        count += 1
        old = n
    # with open(file_path, 'r') as f:
    return output
    