import streamlit as st
import requests
import uuid

st.set_page_config(page_title="AI Support Agent")

# Session State for User ID (simulates login)
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

st.title("🤖 Customer Support AI")
st.caption(f"Session ID: {st.session_state.user_id}")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
if prompt := st.chat_input("How can I help you today?"):
    # 1. Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Call n8n Webhook
    # REPLACE THIS URL with your actual n8n Webhook URL (Test or Production)
    N8N_WEBHOOK_URL = "http://localhost:5678/webhook/customer-message"
    
    with st.spinner("Agent is thinking..."):
        try:
            payload = {
                "message": prompt, 
                "user_id": st.session_state.user_id
            }
            response = requests.post(N8N_WEBHOOK_URL, json=payload)
            
            if response.status_code == 200:
                ai_reply = response.text
            else:
                ai_reply = "Error: Could not connect to AI agent."
                
        except Exception as e:
            ai_reply = f"System Error: {str(e)}"

    # 3. Show AI Response
    with st.chat_message("assistant"):
        st.markdown(ai_reply)
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})