from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth import jwt
from streamlit.web.server.websocket_headers import _get_websocket_headers 

import streamlit as st

st.set_page_config(
    page_title='ROI GenAI Chat',
    page_icon='./static/ROISquareLogo.png',
    layout="wide"
)

def show_intro():
    """
    Displays the introduction section of the ROI Training GenAI Chat page.
    """
    st.image(
        "https://www.roitraining.com/wp-content/uploads/2017/02/ROI-logo.png",
        width=300
    )
    st.title("Auth stuff")

def say_hello(a, b):
    try:
        id_info = id_token.verify_oauth2_token(
            a, 
            requests.Request(), 
            audience=b
        )
        st.write(id_info)
    except ValueError as e:
        st.write(e)

show_intro()
headers = _get_websocket_headers()
st.write(headers)
assertion = headers.get('X-Goog-Iap-Jwt-Assertion')
say_hello(assertion, "168855055138-arrqpas810j6mqt3j8k4o0khqa8m1ue6.apps.googleusercontent.com")
say_hello(assertion, "168855055138-arrqpas810j6mqt3j8k4o0khqa8m1ue6.apps.googleusercontent.com")
