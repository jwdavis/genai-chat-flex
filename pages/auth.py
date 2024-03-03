from langchain.schema import ChatMessage
from langchain_openai import OpenAI, ChatOpenAI
from langchain_google_vertexai import VertexAI
from streamlit.web.server.websocket_headers import _get_websocket_headers 
from urllib.parse import unquote
from config import secrets, PROJECT_ID, PROJECT_NUMBER
from jose import jwt

import asyncio, sys
import streamlit as st

CERTS = None
AUDIENCE = None

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


def certs():
    """Returns a dictionary of current Google public key certificates for
    validating Google-signed JWTs. Since these change rarely, the result
    is cached on first request for faster subsequent responses.
    """
    import requests

    global CERTS
    if CERTS is None:
        response = requests.get(
            'https://www.gstatic.com/iap/verify/public_key'
        )
        CERTS = response.json()
    return CERTS


def audience():
    """Returns the audience value (the JWT 'aud' property) for the current
    running instance. Since this involves a metadata lookup, the result is
    cached when first requested for faster future responses.
    """
    global AUDIENCE
    if AUDIENCE is None:
        project_number = PROJECT_NUMBER
        project_id = PROJECT_ID
        AUDIENCE = '/projects/{}/apps/{}'.format(
            project_number, project_id
        )
    return AUDIENCE

def validate_assertion(assertion):
    """Checks that the JWT assertion is valid (properly signed, for the
    correct audience) and if so, returns strings for the requesting user's
    email and a persistent user ID. If not valid, returns None for each field.
    """
    try:
        info = jwt.decode(
            assertion,
            certs(),
            algorithms=['ES256'],
            audience=audience()
        )
        return info['email'], info['sub']
    except Exception as e:
        print('Failed to validate assertion: {}'.format(e), file=sys.stderr)
        return None, None

def say_hello():
    headers = _get_websocket_headers()
    st.write(headers)
    assertion = headers.get('X-Goog-IAP-JWT-Assertion')
    email, id = validate_assertion(assertion)
    page = "<h1>Hello {}</h1>".format(email)
    st.markdown(page, unsafe_allow_html=True)

show_intro()
say_hello()