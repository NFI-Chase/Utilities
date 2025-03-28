import streamlit as st
from PIL import Image
import io, os
import datetime
import pandas as pd
@st.cache_data
def local_css(file_name):
    with open(file_name) as f: st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
local_css(".//resources//style.css")
@st.cache_data
def load_csv_data():
    df = pd.read_csv(".//resources//detailed_pregnancy_weeks_with_symptoms.csv")
    df.fillna('', inplace=True)
    df = df.astype(str)
    return df
pregnancy_weeks = lambda: load_csv_data()
def compress_image(image, quality):
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG', quality=quality)
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr
st.title("Image Compressor")
st.header("Step 1: Upload Image")
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
fileName = uploaded_file.name if uploaded_file else None
if fileName:
    file_root, file_extension = os.path.splitext(fileName)
    current_date = datetime.datetime.now().strftime("%Y%m%d")    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        st.header("Step 2: Select Compression Options")
        quality = st.slider("Select image quality", 1, 100, 75)

        if st.button("Compress Image"):
            compressed_image = compress_image(image, quality)
            st.image(compressed_image, caption=file_root + "_Compressed_" + current_date, use_container_width=True)

            # Step 4: Download compressed image
            st.header("Step 3: Download Compressed Image")
            st.download_button(
                label="Download Compressed Image",
                data=compressed_image,
                file_name=file_root + "_Compressed_" + current_date +".jpg",
                mime="image/jpeg"
            )
footer='<div class="footer">Developed with <b style="color:red";> ❤ </b> by EvoSoft </br> Sponsor the Creator </br> <a href="https://www.paypal.com/donate/?hosted_button_id=7A4P67BEPT29W" target="_blank">EvoSoft</a></div>'
st.markdown(footer,unsafe_allow_html=True)