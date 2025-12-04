import streamlit as st
import requests
from components.upload import render_uploader
from components.chatUI import render_chat   
from components.history_download import render_history_download


st.set_page_config(page_title="AI Assistant", layout="wide")
st.title("Medical AI Assistant")
render_uploader()
render_chat()
render_history_download()