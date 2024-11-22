import streamlit as st
st.set_page_config(
   page_title="Evosoft Utilities",
   page_icon=":house:",
   layout="wide",
#    initial_sidebar_state="expanded",
)
def app():
    st.title("Utilities")
    st.write("This is the utilities page.")
    st.write("You can use this page to access the utilities that are available in the app.")    

app()