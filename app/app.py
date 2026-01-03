from collections import defaultdict
from dao import (
    auto_name_session,
    clear_history,
    database_init,
    get_all_sessions,
    load_chat,
    rename_session,
    save_message,
    update_reaction
)
from datetime import datetime
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account
import streamlit as st
import time
import uuid

# Initialize database
database_init()

# Initialize session state variables
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "active_session" not in st.session_state:
    st.session_state.active_session = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "animate_last" not in st.session_state:
    st.session_state.animate_last = False

if "start_new_chat" not in st.session_state:
    st.session_state.start_new_chat = False

if "selected_session" not in st.session_state:
    st.session_state.selected_session = "New chat"

# Dialogflow client
PROJECT_ID = st.secrets["DIALOGFLOW_PROJECT_ID"]

@st.cache_resource
def get_dialogflow_client():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["dialogflow_service_account"]
    )
    return dialogflow.SessionsClient(credentials = credentials)
session_client = get_dialogflow_client()

def detect_intent(text: str) -> str:
    session = session_client.session_path(
        PROJECT_ID, st.session_state.session_id
    )

    text_input = dialogflow.TextInput(text = text, language_code = "en")
    query_input = dialogflow.QueryInput(text = text_input)

    response = session_client.detect_intent(
        request = {"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text

# Page configuration
st.set_page_config(
    page_title = "Dialogflow Chatbot",
    page_icon = "🤖",
    layout = "wide",
)
st.sidebar.title("Dialogflow Chatbot")
st.title("Dialogflow Chatbot")
st.caption("Customer support chat interface connecting the Dialogflow chatbot.")

# Sidebar actions
with st.sidebar:
    st.header("Chat Options")

    clear_col, new_col = st.columns(2)

    if clear_col.button("Delete Chat"):
        clear_history(st.session_state.session_id)
        st.session_state.messages = []
        st.session_state.animate_last = False
        st.session_state.start_new_chat = True
        st.rerun()

    if new_col.button("Start New Chat"):
        st.session_state.start_new_chat = True
        st.rerun()

# Apply new chat state before rendering widgets
if st.session_state.start_new_chat:
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.active_session = None
    st.session_state.messages = []
    st.session_state.selected_session = "New chat"
    st.session_state.start_new_chat = False

# Session selector
with st.sidebar:
    st.header("Chat Sessions")

    sessions = get_all_sessions()
    label_to_id = {}
    name_count = defaultdict(int)
    for sid, name in sessions:
        name_count[name] += 1
        label = (
            f"{name} ({name_count[name]})"
            if name_count[name] > 1
            else name
        )
        label_to_id[label] = sid

    st.selectbox(
        "Resume a session",
        options = ["New chat"] + list(label_to_id.keys()),
        key = "selected_session",
    )

    if st.session_state.selected_session != "New chat" and st.session_state.session_id:
        st.text_input(
            label = "Rename Session",
            placeholder = st.session_state.selected_session,
            key = "rename"
        )

        if st.button(
            label = "Rename",
            disabled = not st.session_state.rename.strip() or st.session_state.rename.strip() == "New chat"
        ):
            rename_session(st.session_state.session_id, st.session_state.rename.strip())
            st.session_state.active_session = None
            st.rerun()

# Apply dropdown selection
if st.session_state.selected_session != "New chat":
    selected_id = label_to_id[st.session_state.selected_session]
    if st.session_state.session_id != selected_id:
        st.session_state.session_id = selected_id
        st.session_state.active_session = None

# Load messages when the session changes
if st.session_state.active_session != st.session_state.session_id:
    st.session_state.active_session = st.session_state.session_id
    st.session_state.messages = load_chat(st.session_state.session_id)

# Chat interface
last_index = len(st.session_state.messages) - 1
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.caption(msg["timestamp"])
        if (
            msg["role"] == "assistant"
            and i == last_index
            and st.session_state.animate_last
        ):
            placeholder = st.empty()
            animated = ""
            for ch in msg["content"]:
                animated += ch
                placeholder.markdown(animated)
                time.sleep(0.015)
            st.session_state.animate_last = False
        else:
            st.write(msg["content"])

        if msg["role"] == "assistant":
            c1, c2 = st.columns(2)
            if c1.button("👍", key = f"up_{i}"):
                update_reaction(msg["id"], "up")
                st.session_state.messages = load_chat(
                    st.session_state.session_id
                )
                st.rerun()

            if c2.button("👎", key = f"down_{i}"):
                update_reaction(msg["id"], "down")
                st.session_state.messages = load_chat(
                    st.session_state.session_id
                )
                st.rerun()

            if msg.get("reaction"):
                st.caption(
                    "You reacted 👍"
                    if msg["reaction"] == "up"
                    else "You reacted 👎"
                )

# Quick actions
st.header("Quick actions")
quick_replies = [
    "Track my order",
    "Cancel my order",
    "I need a help",
    "Refund status",
]
cols = st.columns(len(quick_replies))
clicked = None
for col, text in zip(cols, quick_replies):
    if col.button(text):
        clicked = text

# User input handling
user_input = st.chat_input("Type your message...")
final_message = clicked or user_input

if final_message:
    user_time = datetime.now().strftime("%H:%M")
    session_name = "New chat"
    save_message(
        st.session_state.session_id,
        session_name,
        "user",
        final_message,
        user_time,
    )

    auto_name_session(
        st.session_state.session_id,
        final_message
    )

    with st.spinner("Working..."):
        reply = detect_intent(final_message)

    bot_time = datetime.now().strftime("%H:%M")
    save_message(
        st.session_state.session_id,
        session_name,
        "assistant",
        reply,
        bot_time,
    )

    st.session_state.messages = load_chat(
        st.session_state.session_id
    )
    st.session_state.animate_last = True
    st.rerun()