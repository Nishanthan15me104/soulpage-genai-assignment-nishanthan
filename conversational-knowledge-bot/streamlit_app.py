import streamlit as st
import requests

st.set_page_config(
    page_title="Conversational Knowledge Bot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Conversational Knowledge Bot")
st.caption("Streamlit UI → FastAPI → LangChain (Groq)")

API_URL = "http://localhost:8000/chat"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask something...")

if user_input:
    """
    When a user submits a message:
    1. Send the message to the FastAPI backend.
    2. Capture the response and append both to the local chat history.
    3. Display the history on the screen.
    """
    res = requests.post(
        API_URL,
        json={"message": user_input},
        timeout=60
    )

    if res.status_code == 200:
        response = res.json()["response"]
    else:
        response = f"❌ FastAPI error: {res.text}"

    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("assistant", response))

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)
