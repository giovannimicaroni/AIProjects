import streamlit as st
import subprocess
import time
from langserve import RemoteRunnable

if "server_started" not in st.session_state:
    st.session_state["server_process"] = subprocess.Popen(["python", "server.py"])
    time.sleep(2)
    st.session_state["server_started"] = True

remote_chain = RemoteRunnable("http://localhost:8000/translate")

language_from = st.selectbox("Translate From", ["English", "Portuguese", "Spanish", "French", "German", "Italian", "Dutch"])
language_to = st.selectbox("To", ["English", "Portuguese", "Spanish", "French", "German", "Italian", "Dutch"])
text = st.text_area("Enter text to translate:")
button = st.button("Translate")

if button and text:
    answer = remote_chain.invoke({
        "FROM": language_from,
        "TO": language_to,
        "text": text
    })
    st.text_area("Translation", value=answer)