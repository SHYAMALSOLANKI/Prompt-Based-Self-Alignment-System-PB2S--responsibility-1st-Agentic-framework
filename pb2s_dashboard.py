#!/usr/bin/env python3
"""
PB2S Dashboard - Streamlit web interface for the PB2S system
"""

import streamlit as st
import requests
import os
import json      # Used for API response parsing and payloads
import base64   # Used for encoding/decoding audio data
from gtts import gTTS
from io import BytesIO

# --- Page Configuration ---
st.set_page_config(page_title="PB2S Node Dashboard", layout="centered")

# --- CSS Styling ---
st.markdown("""
<style>
.stTextInput>div>div>input {font-size: 1.1rem;}
.stButton>button {font-size: 1.1rem; background-color: #4CAF50; color: white; border-radius: 6px;}
.stMarkdown {font-size: 1.05rem;}
</style>
""", unsafe_allow_html=True)

# --- Friendly AI Avatar and Greeting ---
st.markdown("""
<div style='display: flex; align-items: center; gap: 1.2em;'>
    <img src='https://img.icons8.com/color/96/robot-2.png' width='64' style='border-radius: 50%; box-shadow: 0 2px 8px #ccc;'>
    <div>
        <h1 style='margin-bottom: 0.2em;'>Hi, I'm PB2S Assistant!</h1>
        <span style='font-size:1.1em;'>Ready to help you run, explore, and chat with your distributed AI system. 😊</span>
    </div>
</div>
<br>
""", unsafe_allow_html=True)

# --- User Instructions ---
st.markdown("""
Welcome! This dashboard is your friendly control center for PB2S. Here's what you can do:
• <b>Check if your AI brains are online</b> (main and edge nodes)<br>
• <b>Chat with your AI</b>—ask questions, get help, or just say hi!<br>
• <b>Grow your system</b> by adding more nodes anytime
<br>
<b>How to use:</b>
1. Make sure your PB2S server is running (see below).
2. Type anything you want to ask or say—don't be shy!
3. Click <b>Send</b> and watch your AI respond like a helpful teammate.
4. Add more nodes as your AI family grows!
<br>
<b>To start your PB2S server:</b>
<pre><code>.venv/bin/uvicorn server.main:app --reload --port 8000</code></pre>
<b>To start this dashboard:</b>
<pre><code>.venv/bin/streamlit run pb2s_dashboard.py</code></pre>
""", unsafe_allow_html=True)

# --- Node Configuration ---
NODES = [
    {"name": "Main Brain", "url": os.environ.get("PB2S_MAIN_URL", "http://localhost:8000")},
    # Add more nodes here as needed
]

# --- Node Status and Chat Interface ---
for node in NODES:
    with st.container():
        st.markdown(f"<h2 style='display:inline'>🧠 {node['name']}</h2>", unsafe_allow_html=True)
        # Friendly status check
        try:
            resp = requests.get(node["url"] + "/chat", timeout=2)
            st.success(f"Great news! {node['name']} is online and ready to chat at {node['url']}.")
        except Exception:
            st.error(f"Oops! {node['name']} at {node['url']} is offline or unreachable. I'll keep checking!")
        
        # Conversational chat interface
        st.markdown("<b>Say something to your AI friend:</b>", unsafe_allow_html=True)
        prompt = st.text_input(f"What's on your mind? (Ask anything, or just say hi!)", key=node['name'])
        send_col, resp_col = st.columns([1,3])
        with send_col:
            send = st.button(f"💬 Send to {node['name']}", key=node['name']+"_btn")
        with resp_col:
            if send and prompt.strip():
                with st.spinner("Your AI is thinking..."):
                    try:
                        chat_resp = requests.post(node["url"] + "/chat", json={"message": prompt})
                        if chat_resp.status_code == 200:
                            ai_reply = chat_resp.json()
                            st.success("Here's what your AI says:")
                            # Show as chat bubble
                            st.markdown(f"""
<div style='background:#f0f7ff;padding:1em 1.2em;border-radius:1em;box-shadow:0 1px 4px #e0e0e0;margin-bottom:0.5em;'>
    <b style='color:#1a1a1a;'>🤖 PB2S:</b> <span style='color:#222;font-size:1.08em;'>{ai_reply.get('response', ai_reply)}</span>
</div>
""", unsafe_allow_html=True)
                        else:
                            st.warning(f"Hmm, I couldn't get a response. (Error {chat_resp.status_code})")
                    except Exception as e:
                        st.error(f"Sorry, I ran into a problem: {e}")
        st.markdown("<hr style='margin:1.5em 0;'>", unsafe_allow_html=True)

# --- Knowledge & Creativity Tools ---

# Wikipedia Summary (using Wikipedia API)
st.markdown("""
<hr style='margin:2em 0 1em 0;'>
<h2>📚 Ask Wikipedia</h2>
<span style='font-size:1.08em;'>Type any topic, and PB2S will fetch a summary from Wikipedia (free, copyright-safe).</span>
""", unsafe_allow_html=True)
wiki_query = st.text_input("Wikipedia topic (e.g. Alan Turing, Quantum Computing)", key="wiki_query")
if st.button("Search Wikipedia", key="wiki_btn") and wiki_query.strip():
    with st.spinner("Searching Wikipedia..."):
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_query.strip().replace(' ', '_')}"
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                st.markdown(f"<b>{data.get('title','')}</b><br>{data.get('extract','No summary found.')}", unsafe_allow_html=True)
                if data.get('thumbnail'):
                    st.image(data['thumbnail']['source'], width=200)
            else:
                st.warning("No summary found. Try another topic.")
        except Exception as e:
            st.error(f"Wikipedia error: {e}")

# Translation (LibreTranslate, free endpoint)
st.markdown("""
<hr style='margin:2em 0 1em 0;'>
<h2>🌐 Translate Anything</h2>
<span style='font-size:1.08em;'>Translate text between languages using LibreTranslate (no API key needed, open/free endpoint).</span>
""", unsafe_allow_html=True)
trans_text = st.text_input("Text to translate", key="trans_text")
lang_options = {"English":"en", "Hindi":"hi", "Spanish":"es", "French":"fr", "German":"de", "Chinese":"zh"}
col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("From", list(lang_options.keys()), key="src_lang")
with col2:
    tgt_lang = st.selectbox("To", list(lang_options.keys()), index=1, key="tgt_lang")
if st.button("Translate", key="trans_btn") and trans_text.strip():
    with st.spinner("Translating..."):
        try:
            resp = requests.post("https://libretranslate.de/translate", json={
                "q": trans_text,
                "source": lang_options[src_lang],
                "target": lang_options[tgt_lang],
                "format": "text"
            }, timeout=10)
            if resp.status_code == 200:
                st.success(resp.json().get("translatedText", "No translation returned."))
            else:
                st.warning("Translation failed.")
        except Exception as e:
            st.error(f"Translation error: {e}")

# Text-to-Speech (gTTS, free, copyright-safe)
st.markdown("""
<hr style='margin:2em 0 1em 0;'>
<h2>🗣️ Text to Speech</h2>
<span style='font-size:1.08em;'>Let PB2S read anything aloud using free Google Text-to-Speech (gTTS, copyright-safe for personal use).</span>
""", unsafe_allow_html=True)
tts_text = st.text_input("Text to speak", key="tts_text")
tts_lang = st.selectbox("Language", ["en", "hi", "es", "fr", "de", "zh"], key="tts_lang")
if st.button("Speak", key="tts_btn") and tts_text.strip():
    with st.spinner("Synthesizing speech..."):
        try:
            tts = gTTS(text=tts_text, lang=tts_lang)
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.audio(fp.read(), format='audio/mp3')
        except Exception as e:
            st.error(f"Text-to-speech error: {e}")

# --- Creative Tools: Image Generation (HuggingFace Stable Diffusion) ---
st.markdown("""
<hr style='margin:2em 0 1em 0;'>
<h2>🎨 Create with AI: Image Generation</h2>
<span style='font-size:1.08em;'>Describe anything, and PB2S will paint it for you using open-source AI (Stable Diffusion via HuggingFace). No login or key required.</span>
""", unsafe_allow_html=True)

img_prompt = st.text_input("What image should I create for you? (Describe in detail)", key="img_prompt")
if st.button("Generate Image", key="img_btn") and img_prompt.strip():
    with st.spinner("Painting your imagination with AI..."):
        try:
            api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
            headers = {"accept": "application/json"}
            payload = {"inputs": img_prompt}
            resp = requests.post(api_url, headers=headers, json=payload, timeout=60)
            if resp.status_code == 200 and resp.headers.get('content-type','').startswith('image'):
                st.image(resp.content, caption=f"AI Art: {img_prompt}", use_column_width=True)
            elif resp.status_code == 200 and resp.headers.get('content-type','').startswith('application/json'):
                # Some endpoints return base64 in JSON
                data = resp.json()
                if 'data' in data and isinstance(data['data'], list) and 'b64_json' in data['data'][0]:
                    img_data = base64.b64decode(data['data'][0]['b64_json'])
                    st.image(img_data, caption=f"AI Art: {img_prompt}", use_column_width=True)
                else:
                    st.warning("No image returned. Try a different prompt.")
            else:
                st.warning(f"Image generation failed: {resp.status_code}")
        except Exception as e:
            st.error(f"Image generation error: {e}")

# --- Feature Roadmap & Feedback ---
st.markdown("""
<hr style='margin:2em 0 1em 0;'>
<h2>🚀 Feature Roadmap & Collaboration</h2>
<span style='font-size:1.08em;'>PB2S is a living, collaborative project. Here are upcoming features you can help shape:</span>
<ul style='font-size:1.05em;'>
    <li>🧠 <b>Conversational Memory & Context</b>: Smarter, context-aware chat sessions</li>
    <li>🎤 <b>Voice Input (Speech-to-Text)</b>: Talk to PB2S using your voice</li>
    <li>📄 <b>File Upload & Analysis</b>: Summarize, translate, or ask about your documents</li>
    <li>💻 <b>Code Generation & Execution</b>: Get code snippets, run Python, visualize data</li>
    <li>📚 <b>Personal Knowledge Base</b>: Add your own notes and facts for PB2S to use</li>
    <li>🖼️ <b>Multi-modal Output</b>: Combine text, images, and audio in responses</li>
    <li>🔌 <b>Open Plugin System</b>: Add your own APIs or plugins</li>
    <li>🌍 <b>Accessibility & Internationalization</b>: Screen reader, high-contrast, easy language switch</li>
    <li>🔎 <b>Self-Reflection & Transparency</b>: See PB2S's reasoning and confidence</li>
    <li>🤝 <b>Community & Collaboration</b>: Share creative works, prompts, and responses</li>
</ul>
<br>
<b>What would you like to see first?</b> Use the feedback box below to vote, suggest, or comment!
""", unsafe_allow_html=True)

user_feedback = st.text_area("Your feedback, votes, or feature ideas (optional)", key="user_feedback")
if st.button("Submit Feedback", key="feedback_btn") and user_feedback.strip():
    st.success("Thank you for your feedback! Your ideas help shape PB2S for everyone.")

# --- Footer Tips ---
st.markdown("""
<div style='color:#888;font-size:1.05em;'>
💡 <b>Tip:</b> You can add more nodes or features anytime. This dashboard is designed to grow with you—and your AI is always happy to chat!
</div>
""", unsafe_allow_html=True)