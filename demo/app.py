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
import settings
# Tiêu đề cho ứng dụng
st.title("Nén và giải nén")


option_1 = st.sidebar.selectbox("Chọn phương thức nén", ["Text", "Image"])
option_2 = st.sidebar.selectbox("Chọn thuật toán nén", ["Huffman", "LZM", "Shanon-Fano"])

if option_1 == 'Text':
    # input_text = st.text_area("Nhập văn bản")
    # Hiển thị một file uploader chỉ cho phép tải lên các file văn bản
    uploaded_file_text = st.file_uploader("Chọn một file văn bản", type=["txt"])

    # Tạo button
    
    col1, col2, _, _ = st.columns(4)
    
    button_encode = col1.button("Encode")
    button_decode = col2.button("Decode")
    # Kiểm tra xem người dùng đã tải lên file hay chưa
        
        # Kiểm tra xem button đã được nhấn hay chưa
    if button_encode:
        # Hiển thị nội dung file
        if uploaded_file_text is not None:
            # Đọc nội dung từ file tải lên
            # file_contents = uploaded_file_text.read()
            file_contents = uploaded_file_text.read().decode('utf-8')
            # st.write("Input:",file_contents)

            if option_2 == 'Huffman':
                path = settings.text_dir / uploaded_file_text.name
                # st.write(path)

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
                # st.write(total_2)
                # st.write(output_path)

                
                #     with open(output_path.split('.bin')[0]+'.txt', 'w') as file:
                #         file.write(binary_string)
                # st.write("Input size:", os.stat(path).st_size, "(bytes).")
                # st.write("Output size:", os.stat(output_path).st_size, "(bytes).")
                # st.write("Decode size:", os.stat(uploaded_file_text.name.split('.')[0] + '_decoded.txt').st_size, "(bytes).")
                r = os.stat(path).st_size/os.stat(output_path).st_size
                # st.write("Tỷ số nén:", round(r,5))
                # st.write("Tỷ lệ nén:", round(1/r*100,2), "%")
                # st.write("Hiệu suất nén:", 100-round(1/r*100,2), "%")
                # st.write("Thời gian nén:", round(total_1,5), "(giây).")
                # st.write("Thời gian giải nén:", round(total_2,5), "(giây).")
                data = {
                    'Thông số':["Input size (byte)",'Output size (byte)', "Tỷ số nén", "Tỷ lệ nén (%)", "Hiệu suất nén (%)", "Thời gian nén (s)" ],
                    'Kết quả': [int(os.stat(path).st_size),int(os.stat(output_path).st_size), round(r,5), round(1/r*100,2), 100-round(1/r*100,2), round(total_1,5)]
                }
                # Tạo DataFrame từ dữ liệu
                df = pd.DataFrame(data)

                # Hiển thị bảng
                st.table(df)
                # with open(output_path, "rb") as file:
                #     byte_array = file.read()
                #     # st.write(byte_array)
                #     binary_string = ''.join(format(byte, '08b') for byte in byte_array)
                #     st.write("Output: ",binary_string)
            elif option_2 == 'LZW':
                st.write('Thuật toán LZW')
            else:
                st.write('Thuật toán shannon-fano')
        else:
            st.warning('Vui lòng upload file !!!')
    # if button_decode:
    #     if uploaded_file_text is not None:
    #         if option_2 == 'Huffman':
    #             # st.warning('huffman')
    #             path = settings.text_dir / uploaded_file_text.name
    #             t2 = time.time()
    #             h = Huffman.Huffmancode(path)
    #             h.decompress(settings.text_dir / (uploaded_file_text.name.split('.')[0]+'_encoded.txt'))
    #             t3 = time.time()
    #             total_2 = t3-t2
    #             st.write("Decode size:", os.stat(uploaded_file_text.name.split('.')[0] + '_decoded.txt').st_size, "(bytes).")
    #             st.write(total_2)
    #     else:
    #         st.warning('Vui lòng upload file !!!')
else:
    # Hiển thị một file uploader chỉ cho phép tải lên các file hình ảnh
    uploaded_file = st.file_uploader("Chọn một file ảnh", type=["jpg", "jpeg", "png"])

    # Kiểm tra xem người dùng đã tải lên file hay chưa
    if uploaded_file is not None:
        # Hiển thị ảnh tải lên
        st.image(uploaded_file, caption="Ảnh tải lên", use_column_width=True)

        # Bạn có thể thực hiện các xử lý khác trên ảnh tải lên ở đây
        # Ví dụ: phân tích, xử lý, vẽ biểu đồ, v.v.