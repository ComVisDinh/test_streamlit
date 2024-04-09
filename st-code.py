import streamlit as st
from code_editor import code_editor
import subprocess
import numpy as np

custom_btns = [{
                "name": "Copy",
                "feather": "Copy",
                "alwaysOn": True,
                "commands": ["copyAll"],
                "style": {"top": "0.46rem", "right": "0.4rem"}
                },
               
               {
                "name": "Run",
                "feather": "Play",
                "primary": True,
                "showWithIcon": True,
                "alwaysOn": True,
                "commands": ["submit"],
                "style": {"bottom": "0.44rem", "right": "0.4rem"}
                },]

# css to inject related to info bar
css_string = '''
background-color: #bee1e5;

body > #root .ace-streamlit-dark~& {
   background-color: #262830;
}

.ace-streamlit-dark~& span {
   color: #fff;
   opacity: 0.6;
}

span {
   color: #000;
   opacity: 0.5;
}

.code_editor-info.message {
   width: inherit;
   margin-right: 75px;
   order: 2;
   text-align: center;
   opacity: 0;
   transition: opacity 0.7s ease-out;
}

.code_editor-info.message.show {
   opacity: 0.6;
}

.ace-streamlit-dark~& .code_editor-info.message.show {
   opacity: 0.5;
}
'''
# create info bar dictionary
info_bar = {
  "name": "language info",
  "css": css_string,
  "style": {
            "order": "1",
            "display": "flex",
            "flexDirection": "row",
            "alignItems": "center",
            "width": "100%",
            "height": "2.5rem",
            "padding": "0rem 0.75rem",
            "borderRadius": "8px 8px 0px 0px",
            "zIndex": "9993"
           },
  "info": [{
            "name": "python",
            "style": {"width": "100px"}
           }]
}

with st.sidebar:
    st.markdown("## :heartbeat: :heartbeat: Hướng dẫn  :heartbeat: :heartbeat:")
    st.markdown("1. Đặt tên file (không bắt buộc)")
    st.markdown("2. Viết mã Python vào ô bên dưới")
    st.markdown("3. Nhấn nút **Run** để thực thi mã")
    st.markdown("4. Kết quả sẽ hiển thị ở ô bên dưới")
    st.markdown("5. Bạn có thể tải file Python bằng cách nhấn vào nút **Save file**")
    
    file_name = st.text_input("Tên file:", "st-test.py")
    

# Đặt tên file
col_1, col_2, col_3 = st.columns([0.2, 0.5, 0.4])
with col_2:
    st.title("AIO Code Editor")
with col_3:
    st.image("shark.png", width=150)

response_dict = code_editor("", buttons=custom_btns, height=[10, 30], info=info_bar)

codes = response_dict["text"]   

# ========================= verify ======================
is_execute = True
for line in codes.split('\n'):
    if 'import' in line:
        if 'os' in line:
            is_execute = False


def write_code(code):
    # save code to file
    with open(file_name, "w") as f:
        f.write(codes)
        
# run code
if is_execute == True:
    if response_dict["type"] == "submit":
        st.snow()
        write_code(codes)
        
        # Hiển thị button đownload file
        st.download_button(
            label="Save file",
            data=open(file_name, 'rb').read(),
            file_name= file_name,
            mime="text/plain")
        # Thực thi file Python và lấy đầu ra và lỗi (nếu có)
        result = subprocess.run(['python', file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Hiển thị kết quả trong st.text_area
        st.text_area("Output", result.stdout)
        if result.stderr:
            st.text_area("Error", result.stderr)

else:
    st.text_area("Output", "warning: os is not supported")

    
