import streamlit as st
import auth, history
import hashlib

from datetime import datetime
from config import secrets, load_markdown_files
from streamlit_extras.row import row
from streamlit_extras.stylable_container import stylable_container
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.schema import ChatMessage
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_vertexai import (ChatVertexAI)
from langchain_openai import ChatOpenAI

st.set_page_config(
    page_title='ROI GenAI Chat',
    page_icon='./static/ROISquareLogo.png',
)

MODELS = {
    'Gemini-Pro': 'gemini-pro',
    'PaLMv2': 'chat-bison',
    'GPT-4 Turbo': 'gpt-4-0125-preview',
    'GPT-3.5': 'gpt-3.5-turbo-1106',
    'Codey': 'codechat-bison@002'
}

class StreamHandler(BaseCallbackHandler):
    """
    A callback handler for streaming text updates.

    Args:
        container (Container): The container to display the text updates.
        initial_text (str, optional): The initial text to display. Defaults to "".
    """

    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """
        Callback method called when a new token is received.

        Args:
            token (str): The new token received.
            **kwargs: Additional keyword arguments.
        """
        self.text += token
        self.container.markdown(self.text)

class faux_response():
    def __init__(self, content):
        self.content = content

def clear_chat():
    """
    Clears the chat messages by resetting the 'messages' session state to contain only the initial assistant message.
    """
    st.session_state["messages"] = [ChatMessage(
        role="assistant", content="How can I help you?")]

def load_chat():
    print('loading chat')

def show_sidebar():
    """
    Displays the sidebar with a selectbox to choose a model.
    Updates the session state with the selected model type.
    """
    from streamlit_extras.add_vertical_space import add_vertical_space
    with st.sidebar:
        add_vertical_space(1)
        col1, col2 = st.columns([4, 1])
        with col1:
            if model_type := st.selectbox(
                "Select model",
                (key for key in MODELS.keys()),
                on_change=clear_chat
            ):
                st.session_state['model_type'] = model_type
            
            # chat_metadata = history.get_user_chat_metadata(
            #     auth.get_email(), model_type)
            # chat_history = st.selectbox(
            #     "Chat history",
            #     chat_metadata,
            #     on_change=load_chat(),
            #     placeholder="Select a chat",
            #     index=None
            # )
        with col2:
            st.container(height=14, border=False)
            if st.button("↻", use_container_width=True):
                st.session_state["messages"] = [ChatMessage(
                    role="assistant", content="How can I help you?")]
            st.container(height=13, border=False)
            # st.button("🗑", use_container_width=True)
        # st.divider()
        # st.link_button(
        #     label="Watch Overview Video",
        #     url="https://drive.google.com/file/d/1AUS4iz22fvuj3xRx38JI3YDX06BWDzU_/view?usp=sharing",
        #     type="primary")

def show_intro():
    """
    Displays the introduction section of the GenAI Chat application.
    """
    st.image(
        "https://www.roitraining.com/wp-content/uploads/2017/02/ROI-logo.png",
        width=300
    )
    st.title("Generative AI Playground")
    email=""
    try:
        email = auth.get_email()
    except Exception as e:
        pass
    st.markdown(f"""
        <style>
        .dev_container {{
            border: 2px solid lightgray; /* Light outline */
            border-radius: 10px; /* Rounded corners */
            display: flex; /* Use flexbox to create columns */
            padding: 5px; /* Padding around the content */
            justify-content: space-around; /* Space out the columns evenly */
        }}
        .dev_column {{
            flex: 1; /* Each column takes up equal space */
            padding: 10px; /* Padding around the content of each column */
        }}
        .dev_label {{
            font-weight: bold; /* Make the label bold */
        }}
        </style>
        <div class="dev_container">
        <div class="dev_column">Developer info</div>
        <div class="dev_column">Timestamp: <span class="dev_label">{datetime.now()}</span></div>
        <div class="dev_column">User: <span class="dev_label">{email}</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()


def get_gpt_response():
    """
    Retrieves a response from the GPT model based on the input messages.

    Returns:
        str: The generated response from the GPT model.
    """
    stream_handler = StreamHandler(st.empty())
    chat = ChatOpenAI(
        openai_api_key=secrets['openai_api_key'],
        streaming=True,
        callbacks=[stream_handler],
        model=MODELS[st.session_state['model_type']]
    )
    response = chat.invoke(st.session_state.messages)
    return response


def get_google_response():
    """
    Retrieves a response from the Google Chatbot model based on the current conversation messages.

    Returns:
        str: The response generated by the Google Chatbot model.
    """
    system = """
        You are a large language model. Follow the user's instructions 
        carefully, and where appropriate explain your reasoning. 
        Respond using markdown.
    """
    messages = [
        SystemMessage(content=system) if i == 0
        else HumanMessage(content=msg.content) if msg.role == "user"
        else AIMessage(content=msg.content)
        for i, msg in enumerate(st.session_state.messages)
    ]
    do_streaming = True
    if MODELS[st.session_state['model_type']] == "chat-bison":
        do_streaming = False
    chat = ChatVertexAI(
        model_name=MODELS[st.session_state['model_type']],
        convert_system_message_to_human=True,
        max_output_tokens=2000,
        temperature=0.2,
        streaming=do_streaming,
        callbacks=[StreamHandler(st.empty())]
    )
    try:
        response = chat.invoke(messages)
        if MODELS[st.session_state['model_type']] == "chat-bison":
            response_markdown = response.content
            st.markdown(response_markdown, unsafe_allow_html=True)
    except Exception as e:
        error_type = type(e).__name__
        response = faux_response(
            f"{error_type}: {str(e)}"
        )
        response_markdown = f"""
        <div class="warn_callout">
            <p>There was an error getting the response from the model. 
            <b>{error_type}:<b> {str(e)}</p>
        </div>
        """
        st.markdown(response_markdown, unsafe_allow_html=True)
    return response

def get_hash(prompt):
    """
    Generates a hash from the input prompt.

    Args:
        prompt (str): The prompt to hash.

    Returns:
        str: The hashed value of the input prompt.
    """
    return hashlib.sha256(prompt.encode()).hexdigest()

md_dict = load_markdown_files()
st.markdown(md_dict['styles'], unsafe_allow_html=True)
show_sidebar()
show_intro()
email = auth.get_email()

if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(
        role="assistant", content="How can I help you?")]

for msg in st.session_state["messages"]:
    st.chat_message(msg.role).markdown(msg.content, unsafe_allow_html=True)

if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        if st.session_state['model_type'] in ['PaLMv2', 'Gemini-Pro', 'Codey']:
            with st.spinner("Getting response"):
                response = get_google_response()
        else:
            with st.spinner("Getting response"):
                response = get_gpt_response()

        st.session_state.messages.append(
            ChatMessage(role="assistant",
                        content=response.content)
        )
        # st.session_state.db_info = {
        #     "model": st.session_state['model_type'],
        #     "prompt": st.session_state.messages[1],
        #     "hash": get_hash(st.session_state.messages[1].content),
        #     "messages": st.session_state.messages
        # }
        # history.store_chat(email, st.session_state.db_info)
        # st.rerun()

# st.button("test firestore", on_click=history.test())
# st.button("delete firestore", on_click=history.delete())
