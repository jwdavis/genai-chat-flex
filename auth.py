from google.oauth2 import id_token
from google.auth.transport import requests
from streamlit.web.server.websocket_headers import _get_websocket_headers 
from config import secrets

def get_email():
    email="demo@demo.com"
    headers = _get_websocket_headers()
    assertion = headers.get('X-Goog-Iap-Jwt-Assertion')
    try:
        id_info = id_token.verify_token(
            assertion,
            requests.Request(), 
            audience=secrets['iap_audience'],
            certs_url="https://www.gstatic.com/iap/verify/public_key",
        )
        email = id_info['email']
    except Exception as e:
        pass

    return email