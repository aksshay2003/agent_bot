import streamlit as st
from chatbot_engine import chat_with_graph

st.set_page_config(page_title="LangGraph Groq Chatbot", layout="centered")
st.title("🤖 LangGraph Chatbot with Groq + Tools")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past chat messages
for msg in st.session_state.messages:
    role = msg["type"]
    content = msg["content"]
    with st.chat_message(role):
        st.markdown(content)

# Chat input
user_input = st.chat_input("Say something...")

if user_input:
    # Display and save user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"type": "user", "content": user_input})

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_with_graph(user_input, thread_id="1")
            st.markdown(response)
            st.session_state.messages.append({"type": "assistant", "content": response})
