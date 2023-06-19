import streamlit as st
import pandas as pd
from collections import Counter
from math import log, ceil
from bitstring import BitArray, Bits
import os
import heapq
import time
from tempfile import NamedTemporaryFile

import lib.huffman as Huffman
import lib.lzw as lzw
import lib.shannon as shannon
import settings
# Tiêu đề cho ứng dụng
st.title("Nén và giải nén")

option_2 = st.sidebar.selectbox("Chọn thuật toán nén", ["Huffman", "LZW", "Shanon-Fano"])
# Tạo button

# input_text = st.text_area("Nhập văn bản")
# Hiển thị một file uploader chỉ cho phép tải lên các file văn bản
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

            r = os.stat(path).st_size/os.stat(output_path).st_size

            data = {
                'Thông số':["Input size (byte)",'Output size (byte)', "Tỷ số nén", "Tỷ lệ nén (%)", "Hiệu suất nén (%)", "Thời gian nén (s)" ],
                'Kết quả': [os.stat(path).st_size,os.stat(output_path).st_size, round(r,5), round(1/r*100,2), 100-round(1/r*100,2), round(total_1,5)]
            }
            # Tạo DataFrame từ dữ liệu
            df = pd.DataFrame(data)

            # Hiển thị bảng
            st.table(df)
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
            data2 = {
            'Thông số':["Decode size (byte)",'Thời gian giải nén (s)'],
            'Kết quả': [os.stat(settings.text_dir / (uploaded_file_text.name.split('.')[0] + '_decoded_huffman.txt')).st_size,round(total_2,5)]
            }
            
            # Tạo DataFrame từ dữ liệu
            df2 = pd.DataFrame(data2)

            # Hiển thị bảng
            st.table(df2)
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
    else:
        st.write('Thuật toán shannon-fano')
        output = "encoded_shannon.txt"
        dict_name = "_dict_shannon.csv"
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
            with open(output, "wb") as f:
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
            st.write("Output size:", os.stat(output).st_size, "(bytes).")
            # st.write("Decode size:", os.stat(decode_file).st_size, "(bytes).")
            r = os.stat(path).st_size/os.stat(output).st_size
            st.write("Tỷ số nén:", round(r,5))
            st.write("Tỷ lệ nén:", round(1/r*100,2), "%")
            st.write("Hiệu suất nén:", 100-round(1/r*100,2), "%")
            st.write("Thời gian nén:", round(total_1,5), "(giây).")
            # st.write("Thời gian giải nén:", round(total_2,5), "(giây).")

        if button_decode:
            decode_file = "decoded_shannon.txt"

            t2 = time.time()
            # Read dictionary
            df = pd.read_csv(dict_name,dtype=str,encoding= 'utf-8')
            keys = list(df['keys'])
            values = list(df['values'])
            _dict = dict(zip(keys,values))
            with open(output,'r', encoding='unicode_escape') as f:
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
            file = open(decode_file, 'w')
            file.write(string)
            file.close()
            t3 = time.time()
            total_2 = t3-t2
else:
    st.warning('Vui lòng upload file !!!')

