import pandas as pd
from collections import Counter
from math import log, ceil
from bitstring import BitArray, Bits
import os
import heapq
import time

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