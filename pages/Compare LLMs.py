import streamlit as st
import openai
import open_ai, gemini, non_gemini, claude

from concurrent.futures import ThreadPoolExecutor, as_completed
from streamlit.runtime.scriptrunner import add_script_run_ctx
from config import (
    secrets, 
    text_models,
    gemini_models,
    non_gemini_google_models,
    openai_models,
    claude_models,
    md_dict
)

st.set_page_config(
    page_title='ROI GenAI Chat',
    page_icon='./static/ROISquareLogo.png',
    layout="wide"
)

google_header_style = """
    background-color: #4285f4;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    border-radius: 5px;
    margin-bottom: 10px;
"""

openai_header_style = """
    background-color: rgb(16, 163, 127);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    border-radius: 5px;
    margin-bottom: 10px;
"""

claude_header_style = """
    background-color: #F0EEE5;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    border-radius: 5px;
    margin-bottom: 10px;
"""

st.markdown(md_dict['styles'], unsafe_allow_html=True)

openai.api_key = secrets['openai_api_key']


def show_intro():
    """
    Displays the introduction section of the ROI Training GenAI Chat page.
    """
    st.image(
        "https://www.roitraining.com/wp-content/uploads/2017/02/ROI-logo.png",
        width=300
    )
    st.title("Generative AI Playground - Compare LLMs")
    st.divider()

def get_response(prompt, response_container):
    messages = []
    prompt_message = {
        "role": "user",
        "content": prompt
    }
    system_message = {
        "role": "system",
        "content": f"""You are the ROI Generative AI Chatbot. You provide responses
        that are clear, professional, detailed, and accurate. When asked
        questions, you provide the answer first and then provide additional
        information or context. When specifically prompted to do step-by-step
        reasoning, you do so (as opposed to keeping explanation until the end).
        Your responses should be kept to fewer than 2000 tokens."""
    }
    welcome_message = {
        "role": "assistant",
        "content": "Hi! I'm the ROI Chatbot. How can I help you?"
    }
    messages = [system_message, prompt_message]

    stream = openai.chat.completions.create(
        model=text_models[st.session_state['model_name']], #"gpt-4-0125-preview",
        messages=messages,
        temperature=0.5,
        max_tokens=2048,
        top_p=1,
        n=1,
        stream=True
    )

    response = ""
    try:
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
                response_container.markdown(response, unsafe_allow_html=True)
        response_message = {
            "role": "assistant",
            "content": response
        }
        messages.append(response_message)
        st.session_state['messages'] = messages[2:]
    except Exception as e:
        st.markdown(f"""
            <div class="warn_callout">
                An error occured
            </div>
        """, unsafe_allow_html=True)
        # st.write(e)
    return

show_intro()

cols = [col for col in st.columns(3)]
containers = []
empties = []
for i, model in enumerate(text_models):
    container = cols[i % 3].container(border=True)
    header_style = ""
    if model in gemini_models or model in non_gemini_google_models:
        header_style = google_header_style
    if model in openai_models:
        header_style = openai_header_style
    if model in claude_models:
        header_style = claude_header_style
    container.markdown(
        f"<div style='{header_style}'>{model}</div>",
        unsafe_allow_html=True)
    empty = container.empty()
    containers.append(container)
    empties.append(empty)

prompt = st.chat_input("Your prompt")
if prompt:
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for i, model in enumerate(text_models):
            if model in openai_models:
                future = executor.submit(
                    open_ai.get_response, 
                    prompt, 
                    empties[i], 
                    chat=False, 
                    model_name=text_models[model],
                    parent=containers[i]
                )
                futures.append(future)
            if model in gemini_models:
                future = executor.submit(
                    gemini.get_response, 
                    prompt, 
                    empties[i],
                    chat=False,
                    model_name=text_models[model],
                    parent=containers[i]
                )
                futures.append(future)
            if model in non_gemini_google_models:
                future = executor.submit(
                    non_gemini.get_text_response,
                    prompt,
                    empties[i],
                    model_name=text_models[model],
                    parent=containers[i]
                )
                futures.append(future)
            if model in claude_models:
                future = executor.submit(
                    claude.get_response,
                    prompt,
                    empties[i],
                    chat=False,
                    model_name=text_models[model],
                    parent=containers[i]
                )
                futures.append(future)
        for t in executor._threads:
            add_script_run_ctx(t)

    # for future in as_completed(futures):
    #     future.result()