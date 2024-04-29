from openai import OpenAI
import streamlit as st
from config import secrets
import base64

client = OpenAI(api_key=secrets['openai_api_key'])


def generate_image(prompt, empty, model_name="", parent=None):
    response = None
    error = None
    try:
        with empty:
            with st.spinner("Generating Image..."):
                response = client.images.generate(
                    model=model_name,
                    prompt=prompt,
                    n=1,
                    size="1024x1024",
                    quality="standard",
                    response_format="b64_json"
                )
        image = response.data[0]
        empty.image(base64.b64decode(image.b64_json))
    except Exception as e:
        error = {"error": e}
        empty.json(e)
    return response, error
