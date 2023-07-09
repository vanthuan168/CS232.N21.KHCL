import pandas as pd
from collections import Counter
from math import log, ceil
from bitstring import BitArray, Bits
import os
import heapq
import time
import collections
from PIL import Image
import re
import sys
import re
import numpy as np

def load_file(input):
    with open(input, encoding="utf-8") as f:
        content = f.readlines()
        content = "".join(content)
        if content:
            return content
        else:
            print("Read file failed please try again")
            return ""

hex2bin = dict('{:x} {:04b}'.format(x,x).split() for x in range(16))
def get_bincode(number, places=""):
    if number == 0.0:
        return "0"*places
    hx = float(number).hex()
    p = hx.index('p')
    bn = ''.join(hex2bin.get(char, char) for char in hx[2:p])
    bn = (bn.strip('0'))
    whole, flt = bn.split(".")
    if places == "":
        places = len(flt)+1
    num = int(hx[p+2:])
    whole = "0" * (num - 1) + whole
    output = whole + flt
    if len(output) < places:
      output += "0" * (places - len(output))
    return output[:places]

def generate(char, total, _dict):
    # calculate probability
    probability = [(x[0]/total) for x in char]

    # calculate codework length
    code_length = [(ceil(-log(x,2))) for x in probability]

    # cumulative probability
    cumulative_probability = 0.0
    for i in range(len(code_length)):
        bin_code = get_bincode(cumulative_probability, code_length[i])
        _dict[char[i][1]] = bin_code
        cumulative_probability += probability[i]
    return _dict



# Nén ảnh
def create_list(message):
    list = dict(collections.Counter(message))
    #for key, value in list.items():
        #print(key, ' : ', value)                         #creating the sorted list according to the probablity
    list_sorted = sorted(iter(list.items()), key = lambda k_v:(k_v[1],k_v[0]),reverse=True)
    final_list = []
    for key,value in list_sorted:
        final_list.append([key,value,''])
    return final_list

#print("Shannon tree with merged pathways:")
def divide_list(list):
    if len(list) == 2:
        #print([list[0]],"::",[list[1]])               #printing merged pathways
        return [list[0]],[list[1]]
    else:
        n = 0
        for i in list:
            n+= i[1]
        x = 0
        distance = abs(2*x - n)
        j = 0
        for i in range(len(list)):               #shannon tree structure
            x += list[i][1]
            if distance < abs(2*x - n):
                j = i
    #print(list[0:j+1],"::",list[j+1:])               #printing merged pathways
    return list[0:j+1], list[j+1:]


def label_list(list):
    c = {}
    list1,list2 = divide_list(list)
    for i in list1:
        i[2] += '0'
        c[i[0]] = i[2]
    for i in list2:
        i[2] += '1'
        c[i[0]] = i[2]
    if len(list1)==1 and len(list2)==1:        #assigning values to the tree
        return
    label_list(list2)
    return c

def read_image_to_string(file_path):
    my_string = np.asarray(Image.open(file_path),np.uint8)
    sudhi = my_string
    shape = my_string.shape
    print ("Enetered string is:",my_string)
    stringToEncode = str(my_string.tolist())
    s1 = stringToEncode
    return s1,shape