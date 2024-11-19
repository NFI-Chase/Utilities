import streamlit as st
from cryptography.fernet import Fernet
from PIL import Image
import io

# Generate a key for encryption and decryption
# You must use this key for both encryption and decryption
# key = Fernet.generate_key()
# st.write("Encryption key:", key.decode())

cipher_suite = Fernet(st.secrets["cryptography_key"].encode())

# Function to encrypt a message
def encrypt_message(message):
    encrypted_message = cipher_suite.encrypt(message.encode())
    return encrypted_message

# Function to decrypt a message
def decrypt_message(encrypted_message):
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
    return decrypted_message

# Function to encrypt an image
def encrypt_image(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    encrypted_image = cipher_suite.encrypt(img_byte_arr.getvalue())
    return encrypted_image

# Function to decrypt an image
def decrypt_image(encrypted_image):
    decrypted_image_data = cipher_suite.decrypt(encrypted_image)
    decrypted_image = Image.open(io.BytesIO(decrypted_image_data))
    return decrypted_image

# Streamlit app
st.title("Secret Message Maker")

# Encryption section
st.header("Encryption")
message = st.text_area("Enter a message to encrypt")
if st.button("Encrypt Message"):
    encrypted_message = encrypt_message(message)
    st.text_area("Encrypted Message", encrypted_message.decode())

uploaded_image = st.file_uploader("Choose an image to encrypt", type=["png", "jpg", "jpeg"])
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    if st.button("Encrypt Image"):
        encrypted_image = encrypt_image(image)
        st.text_area("Encrypted Image (Base64)", encrypted_image.decode())

# Decryption section
st.header("Decryption")
encrypted_message_input = st.text_area("Enter an encrypted message to decrypt")
if st.button("Decrypt Message"):
    try:
        decrypted_message = decrypt_message(encrypted_message_input.encode())
        st.text_area("Decrypted Message", decrypted_message)
    except Exception as e:
        st.error(f"Decryption failed: {e}")

encrypted_image_input = st.text_area("Enter an encrypted image (Base64) to decrypt")
if st.button("Decrypt Image"):
    try:
        decrypted_image = decrypt_image(encrypted_image_input.encode())
        st.image(decrypted_image, caption="Decrypted Image", use_container_width=True)
    except Exception as e:
        st.error(f"Decryption failed: {e}")