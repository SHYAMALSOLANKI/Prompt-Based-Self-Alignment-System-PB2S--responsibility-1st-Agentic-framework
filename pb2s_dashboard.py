import streamlit as st
import requests
import os

# Configuration: List of PB2S node endpoints (can be extended to auto-discover)
NODES = [
    {"name": "Main Brain", "url": os.environ.get("PB2S_MAIN_URL", "http://localhost:8000")},
    # Add more nodes as needed
]

st.set_page_config(page_title="PB2S Node Dashboard", layout="wide")
st.title("PB2S Node Dashboard")

for node in NODES:
    st.header(node["name"])
    try:
        resp = requests.get(node["url"] + "/")
        if resp.status_code == 200:
            st.success(f"Node online at {node['url']}")
        else:
            st.warning(f"Node at {node['url']} responded: {resp.status_code}")
    except Exception as e:
        st.error(f"Node at {node['url']} offline or unreachable: {e}")
    # Chat interface
    st.subheader("Send prompt to /chat")
    prompt = st.text_input(f"Prompt for {node['name']}", key=node['name'])
    if st.button(f"Send to {node['name']}", key=node['name']+"_btn"):
        try:
            chat_resp = requests.post(node["url"] + "/chat", json={"message": prompt})
            if chat_resp.status_code == 200:
                st.json(chat_resp.json())
            else:
                st.warning(f"/chat error: {chat_resp.status_code}")
        except Exception as e:
            st.error(f"/chat failed: {e}")
    st.markdown("---")

st.info("Add more nodes or features as needed. This dashboard is fully extensible.")
