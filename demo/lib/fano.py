import pandas as pd
from collections import Counter
from math import log, ceil
from bitstring import BitArray, Bits
import os
import heapq
import time
import collections

def load_file(input):
  with open(input, encoding="utf-8") as f:
    content = f.readlines()
    content = "".join(content)
    if content:
        return content
    else:
        print("Read file failed please try again")
        return ""

def generate(bin_code="", char=[], total=0, _dict={}):
    if len(char) == 1:
        _dict[char[0][1]] = bin_code
        return
    count = char[0][0]
    i = 1
    while True:
        left = count + char[i][0]
        if left*2 > total:
            break
        count += char[i][0]
        i+=1
    generate(bin_code+'0',char[:i],count,_dict)
    generate(bin_code+'1',char[i:],total-count,_dict)


# Nén ảnh
def create_list(message):
    listz = dict(collections.Counter(message))
    # for key, value in list.items():
    #     print(key, ' : ', value)                         #creating the sorted list according to the probablity
    list_sorted = sorted(iter(listz.items()), key = lambda k_v:(k_v[1],k_v[0]),reverse=True)
    final_list = []
    for key,value in list_sorted:
        final_list.append([key,value,''])
    return final_list
# def generate(bin_code="", char=[], total=0, new_dict={}):
#     if len(char) == 1:
#         new_dict[char[0][1]] = bin_code
#         return
#     count = char[0][0]
#     i = 1
#     while True:
#         left = count + char[i][0]
#         if left*2 > total:
#             break
#         count += char[i][0]
#         i+=1
#     generate(bin_code+'0',char[:i],count,new_dict)
#     generate(bin_code+'1',char[i:],total-count,new_dict)
#print("Shannon tree with merged pathways:")
def divide_list(listz):
    if len(listz) == 2:
        # print([list[0]],"::",[list[1]])               #printing merged pathways
        return [listz[0]],[listz[1]]
    else:
        n = 0
        for i in listz:
            n+= i[1]
        x = 0
        distance = abs(2*x - n)
        j = 0
        for i in range(len(listz)):               #shannon tree structure
            x += listz[i][1]
            if distance < abs(2*x - n):
                j = i
    print(listz[0:j+1],"::",listz[j+1:])               #printing merged pathways
    return listz[0:j+1], listz[j+1:]


def label_list(listz):
    c = {}
    list1,list2 = divide_list(listz)
    for i in list1:
        i[2] += '0'
        c[i[0]] = i[2]
    for i in list2:
        i[2] += '1'
        c[i[0]] = i[2]
    if len(list1)==1 and len(list2)==1:        #assigning values to the tree
        return
    label_list(list2)
    print('c la:')
    print(c)
    return c
