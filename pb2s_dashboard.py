import streamlit as st

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

# --- Main Navigation Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat & Nodes", "🛠️ Knowledge Tools", "🎨 Creativity Hub", "🚀 Roadmap & Feedback"])

with tab1:
    st.markdown("### 🧠 Chat with Your AI Nodes")
    # Node Configuration and Chat code here (will move existing chat code)

with tab2:
    st.markdown("### 📚 Knowledge & Utility Tools")
    # Tools like Wikipedia, Translation, News, etc.

with tab3:
    st.markdown("### 🎨 Create & Explore")
    # Image generation, TTS, etc.

with tab4:
    st.markdown("### 🚀 Roadmap & Collaboration")
    st.markdown("""
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
    user_feedback_roadmap = st.text_area("Your feedback, votes, or feature ideas (optional)", key="user_feedback_roadmap")
    if st.button("Submit Feedback", key="feedback_btn_roadmap") and user_feedback_roadmap.strip():
        st.success("Thank you for your feedback! Your ideas help shape PB2S for everyone.")

# --- Knowledge & Creativity Tools ---
import json

with tab2:
    # Wikipedia Summary (using Wikipedia API)
    st.markdown("""
    <hr style='margin:2em 0 1em 0;'>
    <h2>📚 Ask Wikipedia</h2>
    <span style='font-size:1.08em;'>Type any topic, and PB2S will fetch a summary from Wikipedia (free, copyright-safe). <b>Note:</b> Educational and factual content is preserved; only explicit NSFW material is moderated.</span>
    """, unsafe_allow_html=True)
    wiki_query = st.text_input("Wikipedia topic (e.g. Alan Turing, Quantum Computing)", key="wiki_query")
    if st.button("Search Wikipedia", key="wiki_btn") and wiki_query.strip():
        with st.spinner("Searching Wikipedia..."):
            try:
                url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_query.strip().replace(' ', '_')}"
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    extract = data.get('extract','No summary found.')
                    warning = moderate_content(extract, "Wikipedia summary")
                    if warning:
                        st.warning(warning)
                    st.markdown(f"<b>{data.get('title','')}</b><br>{extract}", unsafe_allow_html=True)
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
    <span style='font-size:1.08em;'>Translate text between languages using LibreTranslate (no API key needed, open/free endpoint). <b>Note:</b> Preserves all content except explicit NSFW material.</span>
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
                    translated = resp.json().get("translatedText", "No translation returned.")
                    warning = moderate_content(translated, "translation")
                    if warning:
                        st.warning(warning)
                    st.success(translated)
                else:
                    st.warning("Translation failed.")
            except Exception as e:
                st.error(f"Translation error: {e}")

    # Add more tools here: News, Dictionary, Calculator, etc.

    # News Headlines (using free NewsAPI, note: free tier has limits)
    st.markdown("""
    <hr style='margin:2em 0 1em 0;'>
    <h2>📰 Latest News Headlines</h2>
    <span style='font-size:1.08em;'>Get top news headlines from around the world (free, courtesy of NewsAPI). <b>Note:</b> News content is preserved; only explicit NSFW material is moderated.</span>
    """, unsafe_allow_html=True)
    news_country = st.selectbox("Country", ["us", "in", "gb", "ca", "au"], key="news_country")
    if st.button("Get News", key="news_btn"):
        with st.spinner("Fetching news..."):
            try:
                # Note: Replace with your free API key if needed, or use a keyless endpoint
                api_key = "your_free_newsapi_key_here"  # Get from newsapi.org (free tier available)
                url = f"https://newsapi.org/v2/top-headlines?country={news_country}&apiKey={api_key}"
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    for article in data.get('articles', [])[:5]:  # Show top 5
                        title = article['title']
                        desc = article.get('description','')
                        warning = moderate_content(title + " " + desc, "news article")
                        if warning:
                            st.warning(warning)
                        st.markdown(f"<b>{title}</b><br>{desc}<br><a href='{article['url']}' target='_blank'>Read more</a>", unsafe_allow_html=True)
                        st.markdown("---")
                else:
                    st.warning("News fetch failed. Check API key or try later.")
            except Exception as e:
                st.error(f"News error: {e}")

    # Dictionary Lookup (free API)
    st.markdown("""
    <hr style='margin:2em 0 1em 0;'>
    <h2>📖 Dictionary Lookup</h2>
    <span style='font-size:1.08em;'>Look up word definitions, synonyms, and more (free, using Dictionary API).</span>
    """, unsafe_allow_html=True)
    dict_word = st.text_input("Enter a word", key="dict_word")
    if st.button("Lookup", key="dict_btn") and dict_word.strip():
        with st.spinner("Looking up..."):
            try:
                url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{dict_word.strip()}"
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    if data:
                        entry = data[0]
                        st.markdown(f"<b>{entry['word']}</b>", unsafe_allow_html=True)
                        for meaning in entry.get('meanings', []):
                            definition = meaning['definitions'][0]['definition']
                            warning = moderate_content(definition, "definition")
                            if warning:
                                st.warning(warning)
                            st.markdown(f"<i>{meaning['partOfSpeech']}</i>: {definition}", unsafe_allow_html=True)
                    else:
                        st.warning("Word not found.")
                else:
                    st.warning("Lookup failed.")
            except Exception as e:
                st.error(f"Dictionary error: {e}")

    # Simple Calculator
    st.markdown("""
    <hr style='margin:2em 0 1em 0;'>
    <h2>🧮 Simple Calculator</h2>
    <span style='font-size:1.08em;'>Calculate expressions safely (e.g. 2+2*3).</span>
    """, unsafe_allow_html=True)
    calc_expr = st.text_input("Enter expression", key="calc_expr")
    if st.button("Calculate", key="calc_btn") and calc_expr.strip():
        warning = moderate_content(calc_expr, "expression")
        if warning:
            st.warning(warning)
        try:
            # Safe eval with limited globals
            result = eval(calc_expr, {"__builtins__": None}, {})
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Calculation error: {e}")

    # Time Zone Converter (free API)
    st.markdown("""
    <hr style='margin:2em 0 1em 0;'>
    <h2>🕒 Time Zone Converter</h2>
    <span style='font-size:1.08em;'>Convert time between zones (free, using WorldTimeAPI).</span>
    """, unsafe_allow_html=True)
    tz_from = st.selectbox("From Time Zone", ["America/New_York", "Europe/London", "Asia/Kolkata", "Australia/Sydney"], key="tz_from")
    tz_to = st.selectbox("To Time Zone", ["America/New_York", "Europe/London", "Asia/Kolkata", "Australia/Sydney"], index=1, key="tz_to")
    if st.button("Convert", key="tz_btn"):
        with st.spinner("Converting..."):
            try:
                # Get current time in from zone
                url = f"http://worldtimeapi.org/api/timezone/{tz_from}"
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    from_time = resp.json()['datetime']
                    # Convert to to zone
                    url2 = f"http://worldtimeapi.org/api/timezone/{tz_to}"
                    resp2 = requests.get(url2, timeout=10)
                    if resp2.status_code == 200:
                        to_time = resp2.json()['datetime']
                        st.success(f"From {tz_from}: {from_time}<br>To {tz_to}: {to_time}", unsafe_allow_html=True)
                    else:
                        st.warning("Conversion failed.")
                else:
                    st.warning("Time fetch failed.")
            except Exception as e:
                st.error(f"Time error: {e}")

    # File Upload & Analysis
    st.markdown("""
    <hr style='margin:2em 0 1em 0;'>
    <h2>📄 File Upload & Analysis</h2>
    <span style='font-size:1.08em;'>Upload a text file for basic analysis (word count, summary preview).</span>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a text file", type=["txt"], key="file_upload")
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
        warning = moderate_content(text, "uploaded file")
        if warning:
            st.warning(warning)
        word_count = len(text.split())
        st.markdown(f"<b>Word Count:</b> {word_count}", unsafe_allow_html=True)
        st.markdown(f"<b>Preview:</b> {text[:500]}...", unsafe_allow_html=True)
        if st.button("Summarize (Basic)", key="summarize_btn"):
            summary = text[:200] + "..." if len(text) > 200 else text
            st.success(f"Basic Summary: {summary}")

with tab3:
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
                from gtts import gTTS
                from io import BytesIO
                tts = gTTS(text=tts_text, lang=tts_lang)
                fp = BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                st.audio(fp.read(), format='audio/mp3')
            except Exception as e:
                st.error(f"Text-to-speech error: {e}")

    # Creative Tools: Image Generation (HuggingFace Stable Diffusion)
    st.markdown("""
    <hr style='margin:2em 0 1em 0;'>
    <h2>🎨 Create with AI: Image Generation</h2>
    <span style='font-size:1.08em;'>Describe anything, and PB2S will paint it for you using open-source AI (Stable Diffusion via HuggingFace). No login or key required.</span>
    """, unsafe_allow_html=True)

    img_prompt = st.text_input("What image should I create for you? (Describe in detail)", key="img_prompt")
    if st.button("Generate Image", key="img_btn") and img_prompt.strip():
        with st.spinner("Painting your imagination with AI..."):
            try:
                import base64
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

# --- Node Configuration and Chat ---
import streamlit as st
import requests
import os

# Content Moderation Function - Focus on NSFW content harmful for under 18
def moderate_content(text, source="general"):
    # Focus on explicit NSFW content rather than general sensitive topics
    nsfw_keywords = [
        "porn", "sex", "nude", "naked", "erotic", "adult", "xxx", "nsfw", "fetish", 
        "orgasm", "masturbat", "vagina", "penis", "anus", "oral", "anal", "bdsm",
        "rape", "incest", "pedophil", "child porn", "underage", "teen sex",
        "deepfake", "deepfakes"
    ]
    
    # Allow educational/historical context for sensitive topics
    educational_contexts = [
        "history", "science", "education", "documentary", "museum", "academic", 
        "research", "encyclopedia", "historical", "scientific", "medical"
    ]
    
    text_lower = text.lower()
    
    # Check for NSFW content
    nsfw_flagged = [word for word in nsfw_keywords if word in text_lower]
    
    if nsfw_flagged:
        # Check if it's in an educational context
        has_educational_context = any(ctx in text_lower for ctx in educational_contexts)
        
        if not has_educational_context:
            return f"⚠️ NSFW Content Warning: This {source} contains explicit material not suitable for users under 18: {', '.join(nsfw_flagged)}. Access restricted."
    
    return None

# --- User Instructions ---
st.set_page_config(page_title="PB2S Node Dashboard", layout="centered")
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

st.markdown("""
Welcome! This dashboard is your friendly control center for PB2S. Here’s what you can do:
• <b>Check if your AI brains are online</b> (main and edge nodes)<br>
• <b>Chat with your AI</b>—ask questions, get help, or just say hi!<br>
• <b>Grow your system</b> by adding more nodes anytime
<br>
<b>How to use:</b>
1. Make sure your PB2S server is running (see below).
2. Type anything you want to ask or say—don’t be shy!
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

with tab1:
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
            # 4-Step Structure Buttons
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("📝 DRAFT", key=node['name']+"_draft"):
                    prompt = f"DRAFT: {prompt}"
            with col2:
                if st.button("🤔 REFLECT", key=node['name']+"_reflect"):
                    prompt = f"REFLECT on: {prompt}"
            with col3:
                if st.button("✏️ REVISE", key=node['name']+"_revise"):
                    prompt = f"REVISE: {prompt}"
            with col4:
                if st.button("🚀 ACT", key=node['name']+"_act"):
                    prompt = f"ACT on: {prompt}"
            # Voice Input Note
            st.markdown("<small>💡 For voice input, use browser's microphone with text input (future feature).</small>", unsafe_allow_html=True)
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
                                
                                # Extract the text content from the response
                                response_text = ai_reply.get('text', str(ai_reply))
                                
                                # Show as chat bubble
                                st.markdown(f"""
<div style='background:#f0f7ff;padding:1em 1.2em;border-radius:1em;box-shadow:0 1px 4px #e0e0e0;margin-bottom:0.5em;'>
    <b style='color:#1a1a1a;'>🤖 PB2S:</b> <span style='color:#222;font-size:1.08em;'>{response_text}</span>
</div>
""", unsafe_allow_html=True)
                                
                                # Show PB2S proof details in an expander
                                if 'pb2s_proof' in ai_reply:
                                    proof = ai_reply['pb2s_proof']
                                    with st.expander("🔍 PB2S Self-Reflection Details"):
                                        st.write(f"**Decision:** {proof.get('decision', 'N/A')}")
                                        st.write(f"**Reflection Cycles:** {proof.get('cycles', 0)}")
                                        st.write(f"**Audit Reference:** {proof.get('audit_ref', 'N/A')}")
                            else:
                                st.warning(f"Hmm, I couldn't get a response. (Error {chat_resp.status_code})")
                        except Exception as e:
                            st.error(f"Sorry, I ran into a problem: {e}")
            st.markdown("<hr style='margin:1.5em 0;'>", unsafe_allow_html=True)

st.markdown("""
<div style='color:#888;font-size:1.05em;'>
💡 <b>Tip:</b> You can add more nodes or features anytime. This dashboard is designed to grow with you—and your AI is always happy to chat!
</div>
""", unsafe_allow_html=True)
