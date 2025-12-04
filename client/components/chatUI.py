from config import API_URL
import requests
import streamlit as st
from utils.api import ask_question, upload_pdfs

def render_chat():
    st.subheader("chat with your assistant:")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        st.chat_message(message["role"]).markdown(message["content"])    
    
    ###input and response

    user_input = st.chat_input("Ask your question here:")

    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        response=ask_question(user_input)
        if response.status_code==200:
            answer=response.json().get("response","")
            sources=response.json().get("sources",[])
            st.chat_message("assistant").markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

        else:
            st.error(f"Error: {response.text}")
            