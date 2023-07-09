import streamlit as st
import pandas as pd
from collections import Counter
from math import log, ceil
from bitstring import BitArray, Bits
import os
import heapq
import time
from tempfile import NamedTemporaryFile
import re
import numpy as np
from PIL import Image
import PIL
import collections
import random
import shutil
from collections import defaultdict

import lib.huffman as Huffman
import lib.lzw as lzw
import lib.shannon as shannon
import lib.fano as  fano
import settings

st.set_page_config(
    page_title="Text & Image Compression"
)
# Tiêu đề cho ứng dụng
st.title("Nén và giải nén")

option_1 = st.sidebar.selectbox("Chọn dạng nén",['Text', 'Image'])
option_2 = st.sidebar.selectbox("Chọn thuật toán nén", ["Huffman", "LZW", "Shannon", "Fano"])
# Tạo button

# path_text = st.text_area("Nhập văn bản")
# Hiển thị một file uploader chỉ cho phép tải lên các file văn bản

if option_1 == 'Text':
    option_text = st.radio ('Nhập văn bản hoặc upload file',['Nhập văn bản', 'Upload file'])
    if option_text == 'Nhập văn bản':
        # if "text" not in st.session_state:
        #     st.session_state["text"] = ""
        # text1 = st.text_area('Text : ', st.session_state["text"])
        text = st.text_area('Nhập văn bản tại đây')        
        _,_,col1, col2,_,_= st.columns(6)
        button_encode = col1.button("Encode")
        button_decode = col2.button("Decode")
        if option_2 == 'Huffman':
            if button_encode:
                if text is not None:
                    my_string = text
                    len_my_string = len(my_string)
                    st.write ("Enetered string is:",my_string)
                    st.write("Your data is ",len_my_string * 7 , "bits long")

                    letters = []
                    only_letters = []
                    for letter in my_string:
                        if letter not in letters:
                            frequency = my_string.count(letter)             #frequency of each letter repetition
                            letters.append(frequency)                      
                            letters.append(letter)                        
                            only_letters.append(letter)

                    nodes = []
                    while len(letters) > 0:
                        nodes.append(letters[0:2])
                        letters = letters[2:]                               # sorting according to frequency
                    nodes.sort()
                    huffman_tree = []
                    huffman_tree.append(nodes)                             #Make each unique character as a leaf node

                    def combine_nodes(nodes):
                        pos = 0
                        newnode = []
                        if len(nodes) > 1:
                            nodes.sort()
                            nodes[pos].append("1")                       # assigning values 1 and 0
                            nodes[pos+1].append("0")
                            combined_node1 = (nodes[pos] [0] + nodes[pos+1] [0])
                            combined_node2 = (nodes[pos] [1] + nodes[pos+1] [1])  # combining the nodes to generate pathways
                            newnode.append(combined_node1)
                            newnode.append(combined_node2)
                            newnodes=[]
                            newnodes.append(newnode)
                            newnodes = newnodes + nodes[2:]
                            nodes = newnodes
                            huffman_tree.append(nodes)
                            combine_nodes(nodes)
                        return huffman_tree                                     # huffman tree generation

                    newnodes = combine_nodes(nodes)

                    huffman_tree.sort(reverse = True)
                    # st.success("Huffman tree with merged pathways")

                    checklist = []
                    for level in huffman_tree:
                        for node in level:
                            if node not in checklist:
                                checklist.append(node)
                            else:
                                level.remove(node)
                    count = 0
                    # for level in huffman_tree:
                    #     st.write("Level", count,":",level)             #st.write huffman tree
                    #     count+=1
                    st.write()

                    letter_binary = []
                    if len(only_letters) == 1:
                        lettercode = [only_letters[0], "0"]
                        letter_binary.append(lettercode*len(my_string))
                    else:
                        for letter in only_letters:
                            code =""
                            for node in checklist:
                                if len (node)>2 and letter in node[1]:           #genrating binary code 
                                    code = code + node[2]
                            lettercode =[letter,code]
                            letter_binary.append(lettercode)
                    # st.write(letter_binary)
                    col_df1, col_df2 = st.columns(2)
                    with col_df1:
                        st.write("Binary code generated:")
                        # for letter in letter_binary:
                        #     st.write(letter[0], letter[1])
                        df = pd.DataFrame(letter_binary, columns=['letter', 'code'])
                        
                        df_styled = df.style.hide(axis='index')

                        # Hiển thị bảng
                        # st.dataframe(df_styled)
                        st.table(df)
                    bitstring =""
                    for character in my_string:
                        for item in letter_binary:
                            if character in item:
                                bitstring = bitstring + item[1]
                    binary ="0b"+bitstring
                    # with col_df2:
                        
                    st.write("Your message as binary is:",bitstring)                                         # binary code generated
                        # text = st.text_area('Nhập văn bản tại đây',value=bitstring)
                        
                    # st.session_state["text"] = bitstring          

                    uncompressed_file_size = len(my_string)*7
                    compressed_file_size = len(binary)-2
                    st.write("Your original file size was", uncompressed_file_size,"bits")
                    st.write("The compressed size is:",compressed_file_size)
                    st.write("This is a saving of ",uncompressed_file_size-compressed_file_size,"bits")
                    
                    # output = open("compressed.txt","w+")
                    # st.write("Compressed file generated as compressed.txt")   
                    # output = open("compressed.txt","w+")
                    # st.write("Decoding.......")
                    # output.write(bitstring)
                    # bitstring = str(binary[2:])
                    # uncompressed_string =""
                    # code =""
                    # for digit in bitstring:
                    #     code = code+digit
                    #     pos=0                                        #iterating and decoding
                    #     for letter in letter_binary:
                    #         if code ==letter[1]:
                    #             uncompressed_string=uncompressed_string+letter_binary[pos] [0]
                    #             code=""
                    #         pos+=1

                    # st.write("Your UNCOMPRESSED data is:")
                    # st.write(uncompressed_string)   
                else:
                    st.warning('Vui lòng nhập văn bản !!!')             
            if button_decode:
                if text is not None:
                    my_string = text
                    len_my_string = len(my_string)
                    # st.write ("Enetered string is:",my_string)
                    # st.write("Your data is ",len_my_string * 7 , "bits long")

                    letters = []
                    only_letters = []
                    for letter in my_string:
                        if letter not in letters:
                            frequency = my_string.count(letter)             #frequency of each letter repetition
                            letters.append(frequency)                      
                            letters.append(letter)                        
                            only_letters.append(letter)

                    nodes = []
                    while len(letters) > 0:
                        nodes.append(letters[0:2])
                        letters = letters[2:]                               # sorting according to frequency
                    nodes.sort()
                    huffman_tree = []
                    huffman_tree.append(nodes)                             #Make each unique character as a leaf node

                    def combine_nodes(nodes):
                        pos = 0
                        newnode = []
                        if len(nodes) > 1:
                            nodes.sort()
                            nodes[pos].append("1")                       # assigning values 1 and 0
                            nodes[pos+1].append("0")
                            combined_node1 = (nodes[pos] [0] + nodes[pos+1] [0])
                            combined_node2 = (nodes[pos] [1] + nodes[pos+1] [1])  # combining the nodes to generate pathways
                            newnode.append(combined_node1)
                            newnode.append(combined_node2)
                            newnodes=[]
                            newnodes.append(newnode)
                            newnodes = newnodes + nodes[2:]
                            nodes = newnodes
                            huffman_tree.append(nodes)
                            combine_nodes(nodes)
                        return huffman_tree                                     # huffman tree generation

                    newnodes = combine_nodes(nodes)

                    huffman_tree.sort(reverse = True)
                    # st.write("Huffman tree with merged pathways:")

                    checklist = []
                    for level in huffman_tree:
                        for node in level:
                            if node not in checklist:
                                checklist.append(node)
                            else:
                                level.remove(node)
                    count = 0
                    # for level in huffman_tree:
                    #     st.write("Level", count,":",level)             #st.write huffman tree
                    #     count+=1
                    # st.write()

                    letter_binary = []
                    if len(only_letters) == 1:
                        lettercode = [only_letters[0], "0"]
                        letter_binary.append(lettercode*len(my_string))
                    else:
                        for letter in only_letters:
                            code =""
                            for node in checklist:
                                if len (node)>2 and letter in node[1]:           #genrating binary code 
                                    code = code + node[2]
                            lettercode =[letter,code]
                            letter_binary.append(lettercode)
                    # st.write(letter_binary)
                    # st.write("Binary code generated:")
                    # for letter in letter_binary:
                    #     st.write(letter[0], letter[1])

                    bitstring =""
                    for character in my_string:
                        for item in letter_binary:
                            if character in item:
                                bitstring = bitstring + item[1]
                    binary ="0b"+bitstring
                    # st.write("Your message as binary is:")
                    # st.write(bitstring)                                         # binary code generated
                    # text = st.text_area('Nhập văn bản tại đây',value=bitstring)
                    
                    # st.session_state["text"] = bitstring          
                    
                    uncompressed_file_size = len(my_string)*7
                    compressed_file_size = len(binary)-2
                    # st.write("Your original file size was", uncompressed_file_size,"bits. The compressed size is:",compressed_file_size)
                    # st.write("This is a saving of ",uncompressed_file_size-compressed_file_size,"bits")
                    # output = open("compressed.txt","w+")
                    # st.write("Compressed file generated as compressed.txt")   
                    # output = open("compressed.txt","w+")
                    st.write("Decoding.......")
                    # output.write(bitstring)
                    bitstring = str(binary[2:])
                    uncompressed_string =""
                    code =""
                    for digit in bitstring:
                        code = code+digit
                        pos=0                                        #iterating and decoding
                        for letter in letter_binary:
                            if code ==letter[1]:
                                uncompressed_string=uncompressed_string+letter_binary[pos] [0]
                                code=""
                            pos+=1
                    st.write('Your COMPRESSED data is:', bitstring)
                    st.write("Your UNCOMPRESSED data is:",uncompressed_string)
                    # st.write(uncompressed_string)   
                else:
                    st.warning('Vui lòng nhập văn bản !!!')  
        elif option_2 == 'LZW':
            if button_encode:
                if text is not None:
                    t0 = time.time()
                    st.write('String is ', text)
                    dict_arr,output_code = lzw.encoding_inputtext(text)
                    t1 = time.time()
                    total_1 = t1-t0
                    # lzw.save_binary_file(output_code, 'output.bin')
                    # file_name_encoded = settings.text_dir / (uploaded_file_text.name.split('.')[0] + '_encoded_lzw.txt')
                    # lzw.save_binary_file(output_code, file_name_encoded)
                    df = pd.DataFrame(dict_arr, columns=['String', 'Code'])
                    st.table(df)
                    st.write('Output codes are ',str(output_code))

                    # input_file_size = len(text)  # Kích thước của input file (trước khi mã hóa)
                    # output_file_size = len(output_code)  # Kích thước của output file (sau khi mã hóa)

                    # compression_ratio = input_file_size / output_file_size
                    # st.write("Input size:", input_file_size, "(bytes).")
                    # st.write("Output size:", output_file_size, "(bytes).")
                    # # st.write("Decode size:", os.stat('decode_lzw.txt').st_size, "(bytes).")
                    # r = compression_ratio
                    # st.write("Tỷ số nén:", round(r,5))
                    # st.write("Tỷ lệ nén:", round(1/r*100,2), "%")
                    # st.write("Hiệu suất nén:", 100-round(1/r*100,2), "%")
                    # st.write("Thời gian nén:", round(total_1,5), "(giây).")
                    # st.write("Thời gian giải nén:", round(total_2,5), "(giây).")
                else: 
                    st.warning('Vui lòng nhập văn bản !!!') 
            if button_decode: 
                if text is not None:
                    dict,output_code = lzw.encoding_inputtext(text)
                    t2 = time.time()
                    decode = lzw.decoding_inputtext(output_code)
                    t3 = time.time()
                    total_2 = t3-t2
                    st.write('Your COMPRESSED data is:', str(output_code))
                    st.write("Your UNCOMPRESSED data is:",decode)
                else: 
                    st.warning('Vui lòng nhập văn bản !!!') 
        elif option_2 == 'Shannon':
            if button_encode:
                t0 = time.time()
                # Read file
                # content = load_file(input)
                st.write('Input: ', text)
                content = text

                # Count character
                count = Counter(content)
                total = sum(count.values())
                char = [x[::-1] for x in list(count.items())]
                char.sort(reverse=True)

                # Create dictionary
                _dict = dict()
                shannon.generate(char,total,_dict)

                # Encode
                code = ''
                for c in content:
                    code += _dict[c]
                code_bin = BitArray(bin = code)
                max_bin = len(code)

                # # Save file
                # # output
                # with open(output, "wb") as f:
                #     code_bin.tofile(f)
                # dict
                keys = []
                values = []
                for key in _dict:
                    keys.append(key)
                    values.append(_dict[key])
                encoded = {'keys': list(keys), 'values': list(values)}
                # output = []
                # for c in content:
                #     for key in encoded:
                #         if key == c:
                #             output.append(encoded[key])
                df = pd.DataFrame(encoded)
                # df.to_csv(dict_name, index=False)
                st.write('Dictionary:')
                st.table(df)
                st.write('Output: ', code)
                t1 = time.time()
                total_1 = t1-t0
            if button_decode:
                content = text
                # Count character
                count = Counter(content)
                total = sum(count.values())
                char = [x[::-1] for x in list(count.items())]
                char.sort(reverse=True)

                # Create dictionary
                _dict = dict()
                shannon.generate(char,total,_dict)

                # Encode
                code = ''
                for c in content:
                    code += _dict[c]
                code_bin = BitArray(bin = code)
                max_bin = len(code)

                # # Save file
                # # output
                # with open(output, "wb") as f:
                #     code_bin.tofile(f)
                # dict
                keys = []
                values = []
                for key in _dict:
                    keys.append(_dict[key])
                    values.append(key)
                encoded = {'keys': list(keys), 'values': list(values)}
                # Decode
                string = ''
                s = ''
                for c in code:
                    if s+c not in _dict:
                        s+=c
                    else:
                        string += str(_dict[s+c])
                        s = ''
                print(string)
                st.write('Input: ',code)
                st.write('Output: ',content)
        else:
            if button_encode:
                # Read file
                content = text

                # Count character
                count = Counter(content)
                total = sum(count.values())
                char = [x[::-1] for x in list(count.items())]
                char.sort(reverse=True)

                # Create dictionary
                _dict = dict()
                fano.generate('',char,total,_dict)

                # Encode
                code = ''
                for c in content:
                    code += _dict[c]
                code_bin = BitArray(bin = code)
                max_bin = len(code)

                # Save file
                # output
                # with open(output, "wb") as f:
                #     code_bin.tofile(f)
                # dict
                keys = []
                values = []
                for key in _dict:
                    keys.append(_dict[key])
                    values.append(key)
                encoded = {'keys': list(keys), 'values': list(values)}
                df = pd.DataFrame(encoded)
                st.write('Input: ', content)
                st.write('Dictionary')
                st.table(df)
                st.write('Output: ', code)
            if button_decode:
                content = text

                # Count character
                count = Counter(content)
                total = sum(count.values())
                char = [x[::-1] for x in list(count.items())]
                char.sort(reverse=True)

                # Create dictionary
                _dict = dict()
                fano.generate('',char,total,_dict)

                # Encode
                code = ''
                for c in content:
                    code += _dict[c]
                code_bin = BitArray(bin = code)
                max_bin = len(code)

                keys = []
                values = []
                for key in _dict:
                    keys.append(_dict[key])
                    values.append(key)
                encoded = {'keys': list(keys), 'values': list(values)}
                # Decode
                string = ''
                s = ''
                for c in code:
                    if s+c not in _dict:
                        s+=c
                    else:
                        string+=_dict[s+c]
                        s = ''
                print(string)
                df = pd.DataFrame(encoded)
                st.write('Input: ', code)
                st.write('Output: ', content)
                # st.table(df)
                # st.write('Output: ', code)
    else:
        uploaded_file_text = st.file_uploader("Chọn một file văn bản", type=["txt"])
        _, _ ,col1, col2,_,_= st.columns(6)
        button_encode = col1.button("Encode")
        button_decode = col2.button("Decode")
        # Kiểm tra xem người dùng đã tải lên file hay chưa
        # Kiểm tra xem button đã được nhấn hay chưa

        if uploaded_file_text is not None:
            # Đọc nội dung từ file tải lên
            # file_contents = uploaded_file_text.read()
            file_contents = uploaded_file_text.read().decode('utf-8')
            st.text_area('Nội dung file', value=file_contents, height=200)
            # st.write("Input:",file_contents)
            path = settings.text_dir / uploaded_file_text.name

            if option_2 == 'Huffman':
                if button_encode:
                    # path = settings.text_dir / uploaded_file_text.name
                    
                    h = Huffman.Huffmancode(path)
                    t0 = time.time()
                    output_path = h.compression()
                    t1 = time.time()
                    total_1 = t1-t0
                    # st.write(total_1)

                    # t2 = time.time()
                    # h.decompress(output_path)
                    # t3 = time.time()
                    # total_2 = t3-t2

                    # r = os.stat(path).st_size/os.stat(output_path).st_size

                    # data = {
                    #     'Thông số':["Input size (byte)",'Output size (byte)', "Tỷ số nén", "Tỷ lệ nén (%)", "Hiệu suất nén (%)", "Thời gian nén (s)" ],
                    #     'Kết quả': [os.stat(path).st_size,os.stat(output_path).st_size, round(r,5), round(1/r*100,2), 100-round(1/r*100,2), round(total_1,5)]
                    # }
                    # # Tạo DataFrame từ dữ liệu
                    # df = pd.DataFrame(data)

                    # # Hiển thị bảng
                    # st.table(df)
                    input_file_size = os.path.getsize(path)  # Kích thước của input file (trước khi mã hóa)
                    output_file_size = os.path.getsize(output_path)  # Kích thước của output file (sau khi mã hóa)

                    compression_ratio = input_file_size / output_file_size
                    st.write("Input size:", input_file_size, "(bytes).")
                    st.write("Output size:", output_file_size, "(bytes).")
                    # st.write("Decode size:", os.stat('decode_lzw.txt').st_size, "(bytes).")
                    r = compression_ratio
                    st.write("Tỷ số nén:", round(r,5))
                    st.write("Tỷ lệ nén:", round(1/r*100,2), "%")
                    st.write("Hiệu suất nén:", 100-round(1/r*100,2), "%")
                    st.write("Thời gian nén:", round(total_1,5), "(giây).")
                    # st.write("Thời gian giải nén:", round(total_2,5), "(giây)."
                    st.warning('Nén thành công !!')
                    
                if button_decode:
                    # path = settings.text_dir / uploaded_file_text.name
                    # print(decode_array)
                    h = Huffman.Huffmancode(path)
                    output_path = h.compression()

                    t2 = time.time()
                    h.decompress(output_path)
                    t3 = time.time()
                    total_2 = t3-t2
                    # data2 = {
                    # 'Thông số':["Decode size (byte)",'Thời gian giải nén (s)'],
                    # 'Kết quả': [os.stat(settings.text_dir / (uploaded_file_text.name.split('.')[0] + '_decoded_huffman.txt')).st_size,round(total_2,5)]
                    # }
                    
                    # # Tạo DataFrame từ dữ liệu
                    # df2 = pd.DataFrame(data2)

                    # # Hiển thị bảng
                    # st.table(df2)
                    input_file_size = os.path.getsize(path)  # Kích thước của input file (trước khi mã hóa)
                    output_file_size = os.path.getsize(output_path)  # Kích thước của output file (sau khi mã hóa)

                    compression_ratio = input_file_size / output_file_size
                    
                    st.write("Decode size:", os.stat(settings.text_dir / (uploaded_file_text.name.split('.')[0] + '_decoded_huffman.txt')).st_size, "(bytes).")
                    r = compression_ratio
                    st.write("Thời gian giải nén:", round(total_2,5), "(giây).")
                    st.warning('Giải nén thành công !!')
            elif option_2 == 'LZW':
                if button_encode:
                    t0 = time.time()
                    output_code = lzw.encoding(path)
                    t1 = time.time()
                    total_1 = t1-t0
                    # lzw.save_binary_file(output_code, 'output.bin')
                    file_name_encoded = settings.text_dir / (uploaded_file_text.name.split('.')[0] + '_encoded_lzw.txt')
                    lzw.save_binary_file(output_code, file_name_encoded)


                    input_file_size = os.path.getsize(path)  # Kích thước của input file (trước khi mã hóa)
                    output_file_size = os.path.getsize(file_name_encoded)  # Kích thước của output file (sau khi mã hóa)

                    compression_ratio = input_file_size / output_file_size
                    st.write("Input size:", input_file_size, "(bytes).")
                    st.write("Output size:", output_file_size, "(bytes).")
                    # st.write("Decode size:", os.stat('decode_lzw.txt').st_size, "(bytes).")
                    r = compression_ratio
                    st.write("Tỷ số nén:", round(r,5))
                    st.write("Tỷ lệ nén:", round(1/r*100,2), "%")
                    st.write("Hiệu suất nén:", 100-round(1/r*100,2), "%")
                    st.write("Thời gian nén:", round(total_1,5), "(giây).")
                    # st.write("Thời gian giải nén:", round(total_2,5), "(giây).")

                if button_decode:
                    file_name_decoded = settings.text_dir / (uploaded_file_text.name.split('.')[0] + '_decoded_lzw.txt')

                    output_code = lzw.encoding(path)
                    t2 = time.time()
                    lzw.decoding(output_code, file_name_decoded)
                    t3 = time.time()
                    total_2 = t3-t2
                    input_file_size = os.path.getsize(path)  # Kích thước của input file (trước khi mã hóa)
                    output_file_size = os.path.getsize(file_name_decoded)  # Kích thước của output file (sau khi mã hóa)

                    compression_ratio = input_file_size / output_file_size
                    st.write("Decode size:", os.stat(file_name_decoded).st_size, "(bytes).")
                    r = compression_ratio

                    st.write("Thời gian giải nén:", round(total_2,5), "(giây).")
            elif option_2 == 'Shannon':

                file_name_decoded = settings.text_dir / (uploaded_file_text.name.split('.')[0] + '_decoded_shannon.txt')
                file_name_encoded = settings.text_dir / (uploaded_file_text.name.split('.')[0] + '_encoded_shannon.txt')

                dict_name = settings.text_dir / (uploaded_file_text.name.split('.')[0] +"_dict_shannon.csv")
                max_bin = 0
                if button_encode:
                    t0 = time.time()
                    # Read file
                    content = shannon.load_file(path)

                    # Count character
                    count = Counter(content)
                    total = sum(count.values())
                    char = [x[::-1] for x in list(count.items())]
                    char.sort(reverse=True)

                    # Create dictionary
                    _dict = dict()
                    shannon.generate(char,total,_dict)

                    # Encode
                    code = ''
                    for c in content:
                        code += _dict[c]
                    code_bin = BitArray(bin = code)
                    max_bin = len(code)

                    # Save file
                    # output
                    with open(file_name_encoded, "wb") as f:
                        code_bin.tofile(f)
                    # dict
                    keys = []
                    values = []
                    for key in _dict:
                        keys.append(_dict[key])
                        values.append(key)
                    encoded = {'keys': list(keys), 'values': list(values)}
                    df = pd.DataFrame(encoded)
                    df.to_csv(dict_name, index=False)
                    t1 = time.time()
                    total_1 = t1-t0

                    # In kết quả
                    st.write("Input size:", os.stat(path).st_size, "(bytes).")
                    st.write("Output size:", os.stat(file_name_encoded).st_size, "(bytes).")
                    # st.write("Decode size:", os.stat(decode_file).st_size, "(bytes).")
                    r = os.stat(path).st_size/os.stat(file_name_encoded).st_size
                    st.write("Tỷ số nén:", round(r,5))
                    st.write("Tỷ lệ nén:", round(1/r*100,2), "%")
                    st.write("Hiệu suất nén:", 100-round(1/r*100,2), "%")
                    st.write("Thời gian nén:", round(total_1,5), "(giây).")
                    # st.write("Thời gian giải nén:", round(total_2,5), "(giây).")

                if button_decode:

                    # Read file
                    content = shannon.load_file(path)

                    # Count character
                    count = Counter(content)
                    total = sum(count.values())
                    char = [x[::-1] for x in list(count.items())]
                    char.sort(reverse=True)

                    # Create dictionary
                    _dict = dict()
                    shannon.generate(char,total,_dict)

                    # Encode
                    code = ''
                    for c in content:
                        code += _dict[c]
                    code_bin = BitArray(bin = code)
                    max_bin = len(code)

                    t2 = time.time()
                    # Read dictionary
                    df = pd.read_csv(dict_name,dtype=str,encoding= 'utf-8')
                    keys = list(df['keys'])
                    values = list(df['values'])
                    _dict = dict(zip(keys,values))
                    with open(file_name_encoded,'rb') as f:
                        data = Bits(f)


                    # Decode
                    string = ''
                    s = ''
                    for c in data.bin[:max_bin]:
                        if s+c not in _dict:
                            s+=c
                        else:
                            string+=_dict[s+c]
                            s = ''

                    # Save file
                    file = open(file_name_decoded, 'w', encoding='utf-8')
                    file.write(string)
                    file.close()
                    t3 = time.time()
                    total_2 = t3-t2
                    # In kết quả
                    
                    st.write("Decode size:", os.stat(file_name_decoded).st_size, "(bytes).")
                    r = os.stat(path).st_size/os.stat(file_name_encoded).st_size
            
                    st.write("Thời gian giải nén:", round(total_2,5), "(giây).")
            else:
                file_name_decoded = settings.text_dir / (uploaded_file_text.name.split('.')[0] + '_decoded_fano.txt')
                file_name_encoded = settings.text_dir / (uploaded_file_text.name.split('.')[0] + '_encoded_fano.txt')
                dict_name = settings.text_dir / (uploaded_file_text.name.split('.')[0] +"_dict_fano.csv")
                
                if button_encode:

                    t0 = time.time()
                    # Read file
                    content = fano.load_file(path)

                    # Count character
                    count = Counter(content)
                    total = sum(count.values())
                    char = [x[::-1] for x in list(count.items())]
                    char.sort(reverse=True)

                    # Create dictionary
                    _dict = dict()
                    fano.generate('',char,total,_dict)

                    # Encode
                    code = ''
                    for c in content:
                        code += _dict[c]
                    code_bin = BitArray(bin = code)
                    max_bin = len(code)

                    # Save file
                    # output
                    with open(file_name_encoded, "wb") as f:
                        code_bin.tofile(f)
                    # dict
                    keys = []
                    values = []
                    for key in _dict:
                        keys.append(_dict[key])
                        values.append(key)
                    encoded = {'keys': list(keys), 'values': list(values)}
                    df = pd.DataFrame(encoded)
                    df.to_csv(dict_name, index=False)
                    t1 = time.time()
                    total_1 = t1-t0

                    # Hiển thị kết quả
                    st.write("Input size:", os.stat(path).st_size, "(bytes).")
                    st.write("Output size:", os.stat(file_name_encoded).st_size, "(bytes).")
                    # st.write("Decode size:", os.stat(decode_file).st_size, "(bytes).")
                    r = os.stat(path).st_size/os.stat(file_name_encoded).st_size
                    st.write("Tỷ số nén:", round(r,5))
                    st.write("Tỷ lệ nén:", round(1/r*100,2), "%")
                    st.write("Hiệu suất nén:", 100-round(1/r*100,2), "%")
                    st.write("Thời gian nén:", round(total_1,5), "(giây).")
                    # st._transparent_write("Thời gian giải nén:", round(total_2,5), "(giây).")

                if button_decode:
                    # Read file
                    content = fano.load_file(path)

                    # Count character
                    count = Counter(content)
                    total = sum(count.values())
                    char = [x[::-1] for x in list(count.items())]
                    char.sort(reverse=True)

                    # Create dictionary
                    _dict = dict()
                    fano.generate('',char,total,_dict)

                    # Encode
                    code = ''
                    for c in content:
                        code += _dict[c]
                    code_bin = BitArray(bin = code)
                    max_bin = len(code)
                
                    t2 = time.time()

                    # Read dictionary
                    df = pd.read_csv(dict_name,dtype=str)
                    keys = list(df['keys'])
                    values = list(df['values'])
                    _dict = dict(zip(keys,values))
                    with open(file_name_encoded, 'rb') as f:
                        data = Bits(f)


                    # Decode
                    string = ''
                    s = ''
                    for c in data.bin[:max_bin]:
                        if s+c not in _dict:
                            s+=c
                        else:
                            string+=_dict[s+c]
                            s = ''

                    # Save file
                    file = open(file_name_decoded, 'w', encoding='utf-8')
                    file.write(string)
                    file.close()
                    t3 = time.time()
                    total_2 = t3-t2

                    # Hiển thị kết quả
                    st.write("Decode size:", os.stat(file_name_decoded).st_size, "(bytes).")
                    st.write("Thời gian giải nén:", round(total_2,5), "(giây).")
        else:
            st.warning('Vui lòng upload file !!!')
else:
    uploaded_file_image = st.file_uploader("Chọn một file image", type=["png", "jpg", "jpeg",'bmp'])
    _, _ ,col1, col2,_,_= st.columns(6)
    button_encode = col1.button("Encode")
    button_decode = col2.button("Decode")
    st.write('Nén ảnh')
    if uploaded_file_image is not None:
        path = settings.image_dir / uploaded_file_image.name
        st.image(uploaded_file_image, caption="Hình ảnh đã tải lên")
        if option_2 == 'Huffman':
            encode_file_name = settings.image_dir / (uploaded_file_image.name.split('.')[0] + '_compressed_huffman.txt')
            show_button_download = False
            if button_encode:
                h = Huffman.Huffmancode_img(path)

                t0 = time.time()
                output_path, shape, text, encoded_text= h.compression_img()
                t1 = time.time()
                total_1 = t1 - t0

                uncompressed_file_size = len(text) * 7
                compressed_file_size = len(encoded_text)

                st.write("Your original file size was", uncompressed_file_size,"bits.")
                st.write('The compressed size is:',compressed_file_size,'bits')
                st.write("This is a saving of ",uncompressed_file_size - compressed_file_size,"bits.")
                r = uncompressed_file_size/compressed_file_size
                st.write("Tỷ số nén:", round(r,5))
                st.write("Tỷ lệ nén:", round(1/r*100,2), "%")
                st.write("Hiệu suất nén:", 100-round(1/r*100,2), "%")
                # output = open("compressed_huffman.txt","w+")
                st.write("Compressed file generated as {}".format(encode_file_name))
                st.write("Thời gian nén:", round(total_1,5), "(giây).")
            if button_decode:
                st.write("Decoding.......")
                h = Huffman.Huffmancode_img(path)

                t0 = time.time()
                output_path, shape, text, encoded_text= h.compression_img()
                t1 = time.time()
                total_1 = t1 - t0 

                t2 = time.time()
                decompressed_text = h.decompress_img(output_path)
                t3 = time.time()
                total_2 = t3 - t2

                # Chuyển decompressed_text thành image
                temp = re.findall(r'\d+', decompressed_text)
                res = list(map(int, temp))
                res = np.array(res)
                res = res.astype(np.uint8)
                res = np.reshape(res, shape)
        
                st.write("Observe the shapes and input and output arrays are matching or not")
                st.write("Input image dimensions:",shape)
                st.write("Output image dimensions:",res.shape)
                data = Image.fromarray(res)
                decode_file_name = settings.image_dir / (uploaded_file_image.name.split('.')[0]+'_uncompressed_huffman.jpg')
                data.save(decode_file_name)

                st.success("Success")
                t3 = time.time()
                total_2 = t3-t2
                st.write("Thời gian giải nén:", round(total_2,5), "(giây).")

                col_img_1, col_img_2 = st.columns(2)
                with col_img_1:
                    st.image(uploaded_file_image, caption='Original Image',
                            use_column_width=True)
                with col_img_2:
                    decode_image = PIL.Image.open(decode_file_name)
                    st.image(decode_image, caption='Decoded Image', use_column_width=True)

        elif option_2 == "LZW":
            encode_file_name = settings.image_dir / (uploaded_file_image.name.split('.')[0] + '_compressed_lzw.txt')

            if button_encode:
                s1, shape = lzw.read_image_to_string(path)
                t0 = time.time()
                output_code= lzw.encoding_img(s1)

                # tinh size
                arr_output_code = np.asarray(output_code,np.uint8)
                output_string = " ".join(map(str, arr_output_code.tolist()))
                uncompressed_size = len(s1) * 7
                compressed_size = len(output_string) * 7
                t1 = time.time()
                total_1 = t1-t0
                lzw.save_binary_file(output_code, encode_file_name)

                # Show kết quả 
                r = uncompressed_size/compressed_size
                st.write("Your original file size was", uncompressed_size,"bits.") 
                st.write('The compressed size is:',compressed_size,"bits.")
                st.write("This is a saving of ",uncompressed_size - compressed_size,"bits.")
                st.write("Tỷ số nén:", round(r,5))
                st.write("Tỷ lệ nén:", round(1/r*100,2), "%")
                st.write("Hiệu suất nén:", 100-round(1/r*100,2), "%")
                st.write("Compressed file generated as {}".format(encode_file_name))
                st.write("Thời gian nén:", round(total_1,5), "(giây).")
            if button_decode:
                s1, shape = lzw.read_image_to_string(path)
                decode_file_name = settings.image_dir / (uploaded_file_image.name.split('.')[0] + '_uncompressed_lzw.jpg')

                t2 = time.time()
                Decode_code = lzw.load_binary_file(encode_file_name)
                output = lzw.decoding_img(Decode_code,shape)
                temp = re.findall(r'\d+', output)
                res = list(map(int, temp))
                res = np.array(res)
                res = res.astype(np.uint8)
                res = np.reshape(res, shape)
                
                # show kết quả
                st.write("Decoding.......")
                st.write("Observe the shapes and input and output arrays are matching or not")
                st.write("Input image dimensions:",shape)
                st.write("Output image dimensions:",res.shape)
                data = Image.fromarray(res)
                data.save(decode_file_name)
                t3 = time.time()
                total_2 = t3-t2
                st.write("Thời gian giải nén:", round(total_2,5), "(giây).")

                col_img_1, col_img_2 = st.columns(2)
                with col_img_1:
                    st.image(uploaded_file_image, caption='Original Image',
                            use_column_width=True)
                with col_img_2:
                    decode_image = PIL.Image.open(decode_file_name)
                    st.image(decode_image, caption='Decoded Image', use_column_width=True)
        elif option_2 == 'Shannon':
            encode_file_name = settings.image_dir / (uploaded_file_image.name.split('.')[0] + '_compressed_shannon.txt')
            dict_file_name = settings.image_dir / (uploaded_file_image.name.split('.')[0] + '_dict_shannon.csv')
            if button_encode:
                t0 = time.time()
                # Read file
                content, shape = shannon.read_image_to_string(path)

                # Count character
                count = Counter(content)
                total = sum(count.values())
                char = [x[::-1] for x in list(count.items())]
                char.sort(reverse=True)

                # Create dictionary
                _dict = dict()
                shannon.generate(char,total,_dict)

                # Encode
                code = ''
                for c in content:
                    code += _dict[c]
                code_bin = BitArray(bin = code)
                max_bin = len(code)

                # Save file
                # output
                with open(encode_file_name, "wb") as f:
                    code_bin.tofile(f)
                # dict
                keys = []
                values = []
                for key in _dict:
                    keys.append(_dict[key])
                    values.append(key)
                encoded = {'keys': list(keys), 'values': list(values)}
                df = pd.DataFrame(encoded)
                df.to_csv(dict_file_name, index=False)
                t1 = time.time()
                total_1 = t1-t0
                uncompressed_file_size = len(content)*7
                compressed_file_size = len(code)
                r = uncompressed_file_size/compressed_file_size
                st.write("Your original file size was", uncompressed_file_size,"bits.")
                st.write('The compressed size is:',compressed_file_size,"bits.")
                st.write("This is a saving of ",uncompressed_file_size-compressed_file_size,"bits.")
                # r = uncompressed_file_size/compressed_file_size
                st.write("Tỷ số nén:", round(r,5))
                st.write("Tỷ lệ nén:", round(1/r*100,2), "%")
                st.write("Hiệu suất nén:", 100-round(1/r*100,2), "%")
                st.write("Compressed file generated as {}".format(encode_file_name))
                st.write("Thời gian nén:", round(total_1,5), "(giây).")
            if button_decode:
                #  Decode
                decode_file_name = settings.image_dir / (uploaded_file_image.name.split('.')[0] + '_uncompressed_shannon.jpg')

                content, shape = shannon.read_image_to_string(path)
                t2 = time.time()
                # Read dictionary
                df = pd.read_csv(dict_file_name,dtype=str)
                keys = list(df['keys'])
                values = list(df['values'])
                _dict = dict(zip(keys,values))
                # code = ''
                # st.write(_dict)
                # for c in content:
                #     code += _dict[c]
                # code_bin = BitArray(bin = code)
                # max_bin = len(code)
                with open(encode_file_name,'rb') as f:
                    data = Bits(f)
                # Decode
                string = ''
                s = ''
                for c in data.bin[:len(data)]:
                    if s+c not in _dict:
                        s+=c
                    else:
                        string+=_dict[s+c]
                        s = ''

                # Save file
                temp = re.findall(r'\d+', string)
                res = list(map(int, temp))
                res = np.array(res)
                res = res.astype(np.uint8)
                res = np.reshape(res, shape)
                #print(res)
                st.write("Observe the shapes and input and output arrays are matching or not")
                st.write("Input image dimensions:",shape)
                st.write("Output image dimensions:",res.shape)
                data = Image.fromarray(res)
                data.save(decode_file_name)
                t3 = time.time()
                total_2 = t3-t2
                st.write("Thời gian giải nén:", round(total_2,5), "(giây).")
                st.success("Success")
                col_img_1, col_img_2 = st.columns(2)
                with col_img_1:
                    st.image(uploaded_file_image, caption='Original Image',
                            use_column_width=True)
                with col_img_2:
                    decode_image = PIL.Image.open(decode_file_name)
                    st.image(decode_image, caption='Decoded Image', use_column_width=True)
            
                
        else:
            if button_encode:
                res_2 = Image.open(path)
                my_string = np.asarray(Image.open(path),np.uint8)
                sudhi = my_string
                shape = my_string.shape
                #print ("Enetered string is:",my_string)
                message = str(my_string.tolist())
                
                t0 = time.time()
                c = {}

                count = collections.Counter(message)
                total = sum(count.values())
                char = [x[::-1] for x in list(count.items())]
                code = dict()
                fano.generate('',char,total,code)
                #print("Fano's Encoded Code:")
                encode_file_name = settings.image_dir / (uploaded_file_image.name.split('.')[0] + '_compressed_fano.txt')
                output = open(encode_file_name,"w+")          # generating output binary
                letter_binary = []
                for key, value in code.items():
                    #print(key, ' : ', value)
                    letter_binary.append([key,value])
                # st.write("Compressed file generated as {}".format(encode_file_name))
                i=0
                for a in message:
                    for key, value in code.items():
                        if key in a:
                        #if i<1000:
                            #print(key, ' : ', value)
                            output.write(value)
                        i=i+1
                t1 = time.time()
                total_1 = t1-t0

                t2 = time.time()
                output = open(encode_file_name,"r")
                intermediate = output.readlines()
                bitstring = ""
                for digit in intermediate:
                    bitstring = bitstring + digit
                binary ="0b"+bitstring

                uncompressed_file_size = len(message)*7
                compressed_file_size = len(binary)-2
                r = uncompressed_file_size/compressed_file_size
                st.write("Your original file size was", uncompressed_file_size,"bits.")
                st.write('The compressed size is:',compressed_file_size,"bits.")
                st.write("This is a saving of ",uncompressed_file_size-compressed_file_size,"bits.")
                # r = uncompressed_file_size/compressed_file_size
                st.write("Tỷ số nén:", round(r,5))
                st.write("Tỷ lệ nén:", round(1/r*100,2), "%")
                st.write("Hiệu suất nén:", 100-round(1/r*100,2), "%")
                st.write("Compressed file generated as {}".format(encode_file_name))
                st.write("Thời gian nén:", round(total_1,5), "(giây).")
            if button_decode:
                res_2 = Image.open(path)
                my_string = np.asarray(Image.open(path),np.uint8)
                sudhi = my_string
                shape = my_string.shape
                #print ("Enetered string is:",my_string)
                message = str(my_string.tolist())
                
                t0 = time.time()
                c = {}

                count = collections.Counter(message)
                total = sum(count.values())
                char = [x[::-1] for x in list(count.items())]
                code = dict()
                fano.generate('',char,total,code)
                #print("Fano's Encoded Code:")
                encode_file_name = settings.image_dir / (uploaded_file_image.name.split('.')[0] + '_compressed_fano.txt')
                output = open(encode_file_name,"w+")          # generating output binary
                letter_binary = []
                for key, value in code.items():
                    #print(key, ' : ', value)
                    letter_binary.append([key,value])
                # st.write("Compressed file generated as {}".format(encode_file_name))
                i=0
                for a in message:
                    for key, value in code.items():
                        if key in a:
                        #if i<1000:
                            #print(key, ' : ', value)
                            output.write(value)
                        i=i+1
                t1 = time.time()
                total_1 = t1-t0

                t2 = time.time()
                output = open(encode_file_name,"r")
                intermediate = output.readlines()
                bitstring = ""
                for digit in intermediate:
                    bitstring = bitstring + digit
                binary ="0b"+bitstring

                # uncompressed_file_size = len(message)*7
                # compressed_file_size = len(binary)-2
                # r = uncompressed_file_size/compressed_file_size

                st.write("Decoding.......")

                uncompressed_string =""
                code =""
                for digit in bitstring:
                    code = code+digit
                    pos=0
                    for letter in letter_binary:               # decoding the binary and genrating original data
                        if code ==letter[1]:
                            uncompressed_string=uncompressed_string+letter_binary[pos] [0]
                            code=""
                        pos+=1

                temp = re.findall(r'\d+', uncompressed_string)
                res = list(map(int, temp))
                res = np.array(res)
                res = res.astype(np.uint8)
                res = np.reshape(res, shape)
                #st.write(res)
                st.write("Observe the shapes and input and output arrays are matching or not")
                st.write("Input image dimensions:",shape)
                st.write("Output image dimensions:",res.shape)
                decode_file_name = settings.image_dir / (uploaded_file_image.name.split('.')[0] + '_uncompressed_fano.jpg')
                data = Image.fromarray(res)
                data.save(decode_file_name)
                #if sudhi.all() == res.all():
                st.success("Success")
                t3 = time.time()
                total_2 = t3-t2
                st.write("Thời gian giải nén:", round(total_2,5), "(giây).")
                col_img_1, col_img_2 = st.columns(2)
                with col_img_1:
                    st.image(uploaded_file_image, caption='Original Image',
                            use_column_width=True)
                with col_img_2:
                    decode_image = PIL.Image.open(decode_file_name)
                    st.image(decode_image, caption='Decoded Image', use_column_width=True)
            
    else:
        st.warning('Vui lòng upload file !!!')
