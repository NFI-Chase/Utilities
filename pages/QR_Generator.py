import streamlit as st
import imageio
import base64,os
import io
from io import BytesIO
from PIL import Image, ImageSequence
from amzqr import amzqr
st.set_page_config(
   page_title="QR Code Generator",
   page_icon="",
   layout="wide",
   initial_sidebar_state="expanded",
)
st.title("QR Code Generator (Experimental)")
st.markdown("*I created this page to generate QR codes and GIFs. You can upload an image and generate a QR code with the image embedded in it. You can also generate a GIF with the uploaded images.*")
def remake_qrcode(qr_img, crop_size):
    new_img = qr_img.crop((crop_size, crop_size, qr_img.size[0] - crop_size, qr_img.size[1] - crop_size)) 
    return new_img
def load_qrcode_to_base64(qrLoad, format):
    buf = BytesIO()
    crop_size = 27
    if format == 'jpg':
        qrLoad = qrLoad.crop((crop_size, crop_size, qrLoad.size[0] - crop_size, qrLoad.size[1] - crop_size)) 
        qrLoad.save(buf, format = 'JPG')
        base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
        return "jpg",base64_str
    elif format == 'gif':
        info = qrLoad.info
        sequence = [remake_qrcode(f.copy(), crop_size) for f in ImageSequence.Iterator(qrLoad)]
        sequence[0].save(buf, format='GIF', save_all=True,append_images=sequence[1:], disposal=2,quality=100, **info)
        # base64_str =  f'base64://{base64.b64encode(buf.getvalue()).decode()}'
        url_data = base64.b64encode(buf.getvalue()).decode("utf-8")
        return url_data, buf.getvalue()
saved_qr_name = 'tempQR.gif'

qr_version = st.selectbox('QR Code Version (Size)',(1,2,3,4,5,6,7,8,9,10))
qr_destination_link=st.text_input('QR Data:', key="qrDestinationLink",max_chars=100)
version, level, qr_name = amzqr.run(words=qr_destination_link,version=qr_version,save_name=saved_qr_name,)   
st.image(saved_qr_name)
qr_type = st.selectbox('QR Code Type',('','Automation Color', 'Automation BW'))
if qr_type:
    gif_qr_size=st.number_input('Please Enter the size of QR Image (default: 100):', key="qrSize",value=100, min_value=100, max_value=500, step=50)
    gif_transition_duration=st.number_input('QR Image transition duration (default: 0.30):', key="gifTrasitionDuration",value=0.30, min_value=0.10, max_value=3.5, step=0.20)
    uploaded_files = st.file_uploader("Upload Media File/s:",accept_multiple_files=True, type=['jpg','png','jpeg'])
    if gif_qr_size == '':
        gif_qr_size = 100
    if gif_transition_duration == '':
        gif_transition_duration = 0.30
    images = []
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        image = image.resize((gif_qr_size,gif_qr_size))
        images.append(image)
    if images:
        col1, col2 = st.columns( [0.5, 0.5])
        with col1:
            #do GIF
            st.markdown('<p class="title3">GIF Result</p>', unsafe_allow_html=True)  
            # frames = [Image.open(img) for img in uploaded_files]
            gif_name = 'gifResult.gif'
            images[0].save(gif_name, format='GIF', append_images=images[1:], save_all=True, duration=gif_transition_duration, loop=0)
            st.image(gif_name)
            with open(gif_name, "rb") as file:
                btn = st.download_button(label="Download GIF",
                    data=file, file_name=gif_name, mime="image/gif")
        with col2:
            # do QR
            st.markdown('<p class="title3">QR Code</p>', unsafe_allow_html=True)  
            if qr_type == 'Automation Color' and qr_destination_link and qr_version:
                isColor = True
            elif qr_type == 'Automation BW' and qr_destination_link and qr_version:
                isColor = False 

            imageio.mimsave(gif_name, images, duration=gif_transition_duration)
            amzqr.run(
                words=qr_destination_link,
                version=qr_version,
                level='H',
                picture=gif_name,
                colorized=True,
                contrast=1.0,
                brightness=1.0,
                save_name=saved_qr_name,
                # save_dir="."
            )
            st.image(saved_qr_name, caption="QR Code for the GIF")
        os.remove(gif_name)
        os.remove(saved_qr_name)  
        



