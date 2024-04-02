from langchain.schema import ChatMessage
from langchain_openai import OpenAI, ChatOpenAI
from langchain_google_vertexai import VertexAI

from config import (
    secrets, 
    text_gen_models, 
    md_dict,
    default_model_args
)

import asyncio
import streamlit as st

from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.row import row

st.set_page_config(
    page_title='ROI GenAI Chat',
    page_icon='./static/ROISquareLogo.png',
    layout="wide"
)

MODELS = text_gen_models
st.markdown(md_dict['styles'], unsafe_allow_html=True)
if not st.session_state.get("preferences"):
    prefs = default_model_args["compare"]
    st.session_state["temp"] = str(prefs['temperature'])
    st.session_state["tokens"] = str(prefs['max_tokens'])
    st.session_state["top_p"] = str(prefs['top_p'])

def show_sidebar():
    """
    Displays the sidebar
    """
    with st.sidebar:
        with st.form("preferences", clear_on_submit=False, border=True):

            r1 = row([1,2])
            r1.write("Temp.")
            temp = r1.text_input(
                "Temperature", key="temp", label_visibility="collapsed")
            
            r2 = row([1,2])
            r2.write("Max. Tokens")
            max_tokens = r2.text_input(
                "Max. Tokens", key="tokens", label_visibility="collapsed")
            
            r3 = row([1,2])
            r3.write("Top_P")
            top_p = r3.text_input(
                "Top_P", key="top_p", label_visibility="collapsed")
            
            r4 = row([1, 2])
            r4.write("")
            
            submitted = r4.form_submit_button(
                "Set",
                type="primary",
                use_container_width=True,
                on_click=update_prefs
            )
            
        st.divider()
        add_vertical_space(1)
        st.link_button(
            label="Watch Overview Video",
            url="https://drive.google.com/file/d/1AUS4iz22fvuj3xRx38JI3YDX06BWDzU_/view?usp=sharing",
            type="primary")

def update_prefs ():
    st.write(st.session_state)

def show_intro():
    """
    Displays the introduction section of the ROI Training GenAI Chat page.
    """
    st.image(
        "https://www.roitraining.com/wp-content/uploads/2017/02/ROI-logo.png",
        width=300
    )
    st.title("GenAI Text Generation Comparison")


async def get_response(model_key: str, prompt: str) -> str:
    prompt = f"""
    Follow the user's instructions carefully, answer any questions posed,
    and where appropriate provide step by step explanation of your reasoning. 
    Respond using markdown. Please respond to the following prompt:

    {prompt}
    """
    if model_key in ['PaLM', 'Gemini 1.0 Pro', 'Codey']:
        model_name = MODELS[model_key]
        llm = VertexAI(model_name=model_name)
        response = llm.generate([prompt])
        return response
    elif model_key == 'GPT-3.5':
        model_name = MODELS[model_key]
        chat = OpenAI(
            openai_api_key=secrets['openai_api_key'],
            model=model_name
        )
        response = await chat.ainvoke(prompt)
        return response
    elif model_key == 'GPT-4 Turbo':
        model_name = MODELS[model_key]
        chat = ChatOpenAI(
            openai_api_key=secrets['openai_api_key'],
            model=model_name
        )
        messages = [
            ChatMessage(role="assistant", content="How can I help you?"),
            ChatMessage(role="user", content=prompt)
        ]
        response = await chat.ainvoke(messages)
        return response.content
    
async def update_tab(tab, prompt, result, empty):
    empty.empty()
    tab.chat_message("user").markdown(prompt, unsafe_allow_html=True)

    if hasattr(result, "generations"):
        response = result.generations[0][0].dict()["text"]
        tab.chat_message("ai").markdown(response, unsafe_allow_html=True)
        with tab.chat_message("user", avatar="💡"):
            info = result.generations[0][0].dict()
            del info["text"]
            del info["type"]
            st.write("Additional info returned by the API")
            st.write(info)
    else:
        tab.chat_message("ai").markdown(result, unsafe_allow_html=True)


async def main():
    show_sidebar()
    show_intro()

    tabs = st.tabs(MODELS.keys())
    empties = []
    prompt = st.chat_input("Your prompt")
    if prompt:
        tasks = []
        for i, model_key in enumerate(MODELS.keys()):
            with tabs[i]:
                empty = st.empty()
                with empty:
                    if not "soon" in model_key:
                        st.status(f"Getting response from {model_key}...")
                    else:
                        st.write(f"{model_key} is coming soon")
                empties.append(empty)

            async def update_tab_coroutine(tab, prompt, result, empty):
                await update_tab(tab, prompt, result, empty)

            if not "soon" in model_key:
                task = asyncio.create_task(get_response(model_key, prompt))
                task.add_done_callback(
                    lambda t, i=i: asyncio.create_task(
                        update_tab_coroutine(
                            tabs[i], 
                            prompt, 
                            t.result(), 
                            empties[i]
                        )
                    )
                )
                tasks.append(task)
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
