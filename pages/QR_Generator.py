import streamlit as st
import imageio
import base64,os
import io
from  PIL import Image
from amzqr import amzqr
def load_qrcode_to_base64(qrLoad, format):
    buf = BytesIO()
    if format == 'jpg':
        crop_size = 27
        qrLoad = qrLoad.crop((crop_size, crop_size, qrLoad.size[0] - crop_size, qrLoad.size[1] - crop_size)) 
        qrLoad.save(buf, format = 'JPG')
        base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
        return base64_str
st.markdown('<p class="fontPageHeadings">QR Code Generator</p>', unsafe_allow_html=True)
uploaded_files = st.file_uploader("",accept_multiple_files=True, type=['jpg','png','jpeg'])
col1, col2 = st.columns( [0.5, 0.5])
with col1:
    gif_qr_size=st.number_input(label='Please Enter the size of Image (default: 100):', key="qrSize",value=100, min_value=100, max_value=500, step=50)
    gif_transition_duration=st.number_input(label='GIF transition duration (default: 0.30):', key="gifTrasitionDuration",value=0.30, min_value=0.10, max_value=3.5, step=0.20)
with col2:
    qr_type = st.selectbox('QR Code Type',('','Automation Color', 'Automation BW', 'Plain QR'))
    qr_version = st.selectbox('QR Code Version (Size)',(1,2,3,4,5,6,7,8,9,10))
    qr_destination_link=st.text_input(label='QR Data:', key="qrDestinationLink",max_chars=100)
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
        output = io.BytesIO()
        imageio.mimwrite(output, images, "gif", duration=gif_transition_duration)
        data_url = base64.b64encode(output.getvalue()).decode("utf-8")
        imageio.mimsave('gifResult.gif', images, duration=gif_transition_duration)
        st.markdown(f'</br> <img src="data:image/gif;base64,{data_url}" alt="Output GIF">',unsafe_allow_html=True,)
        st.download_button(label='Download GIF', data=output, file_name='gifResult.gif', mime='image/gif' )
    with col2:
        #do QR
        if qr_type != '' and qr_version != '' and qr_destination_link != '':
            saved_qr_name = 'tempQR.gif'
            st.markdown('<p class="title3">QR Code Result</p>', unsafe_allow_html=True)
            if qr_type == 'Automation Color' and qr_destination_link and qr_version:
                version, level, qr_name = amzqr.run(words=qr_destination_link,version=qr_version,level='H',picture="gifResult.gif", colorized=True,contrast=1.0,brightness=1.0,save_name=saved_qr_name)
                qrLoad = Image.open(saved_qr_name)
                data_url, data = load_qrcode_to_base64(qrLoad, 'gif')
                st.markdown(f'</br> <img src="data:image/gif;base64,{data_url}" alt="Output QR">',unsafe_allow_html=True,)
                st.download_button(label='Download QR Code', data=data, file_name='qrCodeResult.gif', mime='image/gif' )
                if qrLoad : qrLoad.close()
            elif qr_type == 'Automation BW' and qr_destination_link and qr_version:
                version, level, qr_name = amzqr.run(words=qr_destination_link,version=qr_version,level='H',picture="gifResult.gif", colorized=False,contrast=1.0,brightness=1.0,save_name=saved_qr_name)
            elif qr_type == 'Plain QR'and qr_destination_link:
                version, level, qr_name = amzqr.run(words=qr_destination_link,save_name=saved_qr_name,)
            os.remove('gifResult.gif')
            os.remove(saved_qr_name)