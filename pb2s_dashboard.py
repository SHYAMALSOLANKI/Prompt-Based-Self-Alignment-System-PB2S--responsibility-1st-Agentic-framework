# Fix for Streamlit metadata issues in PyInstaller
try:
    import streamlit_fix_hook
except ImportError:
    pass

import streamlit as st
import requests
import os
import base64

# Import KoboldAI CPP, llama.cpp and LM Studio connectors
try:
    from kobold_connector import KoboldAICPPConnector
    KOBOLD_AVAILABLE = True
except ImportError:
    KOBOLD_AVAILABLE = False
    print("⚠️  KoboldAI connector not available")

try:
    from llama_cpp_connector import LlamaCPPConnector
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False
    print("⚠️  llama.cpp connector not available")

try:
    from lmstudio_connector import LMStudioConnector
    LMSTUDIO_AVAILABLE = True
except ImportError:
    LMSTUDIO_AVAILABLE = False
    print("⚠️  LM Studio connector not available")

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

# Page configuration
st.set_page_config(
    page_title="PB2S Dashboard", 
    page_icon="🧠", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.markdown("""
<div style='text-align: center; padding: 1rem 0; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 2rem;'>
    <h1 style='margin: 0; font-size: 2.5rem;'>🧠 PB2S Dashboard</h1>
    <p style='margin: 0; font-size: 1.2rem; opacity: 0.9;'>Prompt-Based Self-Alignment System</p>
</div>
""", unsafe_allow_html=True)

# Main Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat & Nodes", "🛠️ Knowledge Tools", "🎨 Creativity Hub", "🚀 Roadmap & Feedback"])

with tab1:
    st.markdown("### 🧠 Chat with Your AI Nodes")
    
    # User Instructions
    st.markdown("""
    <div style='background:#e8f4f8;padding:1em;border-radius:0.5em;margin-bottom:1em;'>
        <b>💡 How to use PB2S Chat:</b><br>
        1. Your AI nodes are automatically configured below<br>
        2. Type any question or prompt in the text box<br>
        3. Click "Send" to get AI responses with PB2S self-reflection<br>
        4. Use the 4-step buttons for specific PB2S workflow stages
    </div>
    """, unsafe_allow_html=True)

    # Node Configuration - Enhanced with Local Models
    nodes = [
        {"name": "Main Brain", "url": "http://127.0.0.1:8000", "role": "🎯 Main reasoning and conversation", "type": "api"},
        {"name": "Local Model (LM Studio)", "url": "http://localhost:1234", "role": "🎨 LM Studio with Mistral", "type": "lmstudio"},
        {"name": "Local Model (llama.cpp)", "url": "http://localhost:8080", "role": "🦙 llama.cpp built from source", "type": "llama_cpp"},
        {"name": "Local Model (KoboldAI)", "url": "http://localhost:5001", "role": "🤖 KoboldAI CPP alternative", "type": "kobold"}
    ]

    # Initialize connectors if available
    kobold_connector = None
    llama_cpp_connector = None
    lmstudio_connector = None
    
    if KOBOLD_AVAILABLE:
        kobold_connector = KoboldAICPPConnector()
    if LLAMA_CPP_AVAILABLE:
        llama_cpp_connector = LlamaCPPConnector()
    if LMSTUDIO_AVAILABLE:
        lmstudio_connector = LMStudioConnector()

    for i, node in enumerate(nodes):
        st.markdown(f"<h3 style='display:inline'>🧠 {node['name']}</h3> - {node['role']}", unsafe_allow_html=True)
        
        # Status check - Different for API vs Local Models
        if node["type"] == "kobold" and kobold_connector:
            status = kobold_connector.check_connection()
            if status["status"] == "online":
                st.success(f"✅ {node['name']} is online - Model: {status.get('model', 'Unknown')} at {node['url']}")
            else:
                st.error(f"❌ {node['name']} at {node['url']} is {status['status']} - {status.get('message', '')}")
                if status["status"] == "offline":
                    st.info("💡 To start KoboldAI CPP: Download model → Run: ./koboldcpp --port 5001 your_model.gguf")
        elif node["type"] == "llama_cpp" and llama_cpp_connector:
            status = llama_cpp_connector.check_connection()
            if status["status"] == "online":
                st.success(f"✅ {node['name']} is online - Model: {status.get('model', 'Unknown')} at {node['url']}")
            else:
                st.error(f"❌ {node['name']} at {node['url']} is {status['status']} - {status.get('message', '')}")
                if status["status"] == "offline":
                    st.info("💡 To start llama.cpp: Build from source → Run: ./server --port 8080 -m your_model.gguf")
        elif node["type"] == "lmstudio" and lmstudio_connector:
            status = lmstudio_connector.check_connection()
            if status["status"] == "online":
                st.success(f"✅ {node['name']} is online - Model: {status.get('model', 'Unknown')} at {node['url']}")
            else:
                st.error(f"❌ {node['name']} at {node['url']} is {status['status']} - {status.get('message', '')}")
                if status["status"] == "offline":
                    st.info("💡 To start LM Studio: Open LM Studio → Load Model → Start Server")
        else:
            # Original API status check
            try:
                resp = requests.get(node["url"] + "/chat", timeout=2)
                st.success(f"✅ {node['name']} is online and ready at {node['url']}")
            except Exception:
                st.error(f"❌ {node['name']} at {node['url']} is offline or unreachable")
        
        # Chat interface
        st.markdown(f"**Chat with {node['name']}:**")
        prompt = st.text_input(f"What would you like to ask {node['name']}?", key=f"{node['name']}_prompt")
        
        # 4-Step Structure Buttons
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📝 DRAFT", key=f"{node['name']}_draft"):
                prompt = f"DRAFT: {prompt}"
        with col2:
            if st.button("🤔 REFLECT", key=f"{node['name']}_reflect"):
                prompt = f"REFLECT on: {prompt}"
        with col3:
            if st.button("✏️ REVISE", key=f"{node['name']}_revise"):
                prompt = f"REVISE: {prompt}"
        with col4:
            if st.button("🚀 ACT", key=f"{node['name']}_act"):
                prompt = f"ACT on: {prompt}"
        
        # Send button and response - Enhanced for both API and KoboldAI
        if st.button(f"💬 Send to {node['name']}", key=f"{node['name']}_send") and prompt.strip():
            with st.spinner(f"🧠 {node['name']} is thinking..."):
                try:
                    if node["type"] == "kobold" and kobold_connector:
                        # Handle KoboldAI CPP
                        result = kobold_connector.generate_pb2s_response(prompt)
                        
                        if result["success"]:
                            # Format and display KoboldAI response
                            formatted_response = kobold_connector.format_pb2s_response(result["response"])
                            
                            # Display response in a nice chat bubble
                            st.markdown(f"""
<div style='background:#f0f7ff;padding:1em 1.2em;border-radius:1em;box-shadow:0 1px 4px #e0e0e0;margin:1em 0;'>
    <b style='color:#1a1a1a;'>🤖 {node['name']} (KoboldAI):</b><br>
    <pre style='color:#222;font-size:1.1em;line-height:1.5;white-space:pre-wrap;font-family:inherit;'>{formatted_response}</pre>
</div>
""", unsafe_allow_html=True)
                            
                            # Show additional info
                            with st.expander("🔍 KoboldAI Model Details"):
                                st.write(f"**Model Info**: {result['model_info']}")
                                st.write(f"**Raw Response Length**: {len(result.get('raw_text', ''))}")
                                if st.checkbox("Show Raw Response", key=f"{node['name']}_raw"):
                                    st.text(result.get('raw_text', 'No raw text available'))
                        else:
                            st.error(f"❌ {node['name']} Error: {result['error']}")
                            if "fallback" in result:
                                st.warning("🔄 Using fallback response:")
                                fallback_response = kobold_connector.format_pb2s_response(result["fallback"])
                                st.text(fallback_response)
                                
                    elif node["type"] == "llama_cpp" and llama_cpp_connector:
                        # Handle llama.cpp
                        result = llama_cpp_connector.generate_pb2s_response(prompt)
                        
                        if result["success"]:
                            # Format and display llama.cpp response
                            formatted_response = llama_cpp_connector.format_pb2s_response(result["response"])
                            
                            # Display response in a nice chat bubble
                            st.markdown(f"""
<div style='background:#f0fff0;padding:1em 1.2em;border-radius:1em;box-shadow:0 1px 4px #e0e0e0;margin:1em 0;'>
    <b style='color:#1a1a1a;'>🦙 {node['name']} (llama.cpp):</b><br>
    <pre style='color:#222;font-size:1.1em;line-height:1.5;white-space:pre-wrap;font-family:inherit;'>{formatted_response}</pre>
</div>
""", unsafe_allow_html=True)
                            
                            # Show additional info
                            with st.expander("🔍 llama.cpp Model Details"):
                                st.write(f"**Model Info**: {result['model_info']}")
                                st.write(f"**Raw Response Length**: {len(result.get('raw_text', ''))}")
                                if st.checkbox("Show Raw Response", key=f"{node['name']}_raw_llama"):
                                    st.text(result.get('raw_text', 'No raw text available'))
                        else:
                            st.error(f"❌ {node['name']} Error: {result['error']}")
                            if "fallback" in result:
                                st.warning("🔄 Using fallback response:")
                                fallback_response = llama_cpp_connector.format_pb2s_response(result["fallback"])
                                st.text(fallback_response)
                                
                    elif node["type"] == "lmstudio" and lmstudio_connector:
                        # Handle LM Studio
                        result = lmstudio_connector.generate_pb2s_response(prompt)
                        
                        if result["success"]:
                            # Format and display LM Studio response
                            formatted_response = lmstudio_connector.format_pb2s_response(result["response"])
                            
                            # Display response in a nice chat bubble
                            st.markdown(f"""
<div style='background:#fff8f0;padding:1em 1.2em;border-radius:1em;box-shadow:0 1px 4px #e0e0e0;margin:1em 0;'>
    <b style='color:#1a1a1a;'>🎨 {node['name']} (LM Studio):</b><br>
    <pre style='color:#222;font-size:1.1em;line-height:1.5;white-space:pre-wrap;font-family:inherit;'>{formatted_response}</pre>
</div>
""", unsafe_allow_html=True)
                            
                            # Show additional info
                            with st.expander("🔍 LM Studio Model Details"):
                                st.write(f"**Model Info**: {result['model_info']}")
                                st.write(f"**Raw Response Length**: {len(result.get('raw_text', ''))}")
                                if st.checkbox("Show Raw Response", key=f"{node['name']}_raw_lmstudio"):
                                    st.text(result.get('raw_text', 'No raw text available'))
                        else:
                            st.error(f"❌ {node['name']} Error: {result['error']}")
                            if "fallback" in result:
                                st.warning("🔄 Using fallback response:")
                                fallback_response = lmstudio_connector.format_pb2s_response(result["fallback"])
                                st.text(fallback_response)
                                
                    else:
                        # Handle regular API (original code)
                        chat_resp = requests.post(node["url"] + "/chat", json={"message": prompt}, timeout=30)
                        if chat_resp.status_code == 200:
                            ai_reply = chat_resp.json()
                            
                            # Extract text content
                            response_text = ai_reply.get('text', str(ai_reply))
                            
                            # Display response in a nice chat bubble
                            st.markdown(f"""
<div style='background:#f0f7ff;padding:1em 1.2em;border-radius:1em;box-shadow:0 1px 4px #e0e0e0;margin:1em 0;'>
    <b style='color:#1a1a1a;'>🤖 {node['name']}:</b><br>
    <span style='color:#222;font-size:1.1em;line-height:1.5;'>{response_text}</span>
</div>
""", unsafe_allow_html=True)
                            
                            # Show PB2S proof details
                            if 'pb2s_proof' in ai_reply:
                                proof = ai_reply['pb2s_proof']
                                with st.expander("🔍 PB2S Self-Reflection Details"):
                                    st.json(proof)
                                    
                        else:
                            st.error(f"❌ Error {chat_resp.status_code}: {chat_resp.text}")
                            
                except Exception as e:
                    st.error(f"❌ Connection error: {str(e)}")
        
        st.markdown("---")

with tab2:
    st.markdown("### 📚 Knowledge & Utility Tools")
    
    # Wikipedia Summary
    st.markdown("""
    <h4>📖 Wikipedia Summary</h4>
    <span style='font-size:1.1em;'>Get instant summaries from Wikipedia on any topic.</span>
    """, unsafe_allow_html=True)
    
    wiki_query = st.text_input("Enter a topic to research:", key="wiki_query")
    if st.button("🔍 Search Wikipedia", key="wiki_btn") and wiki_query.strip():
        warning = moderate_content(wiki_query, "search topic")
        if warning:
            st.warning(warning)
        else:
            with st.spinner("Fetching Wikipedia summary..."):
                try:
                    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_query.strip().replace(' ', '_')}"
                    resp = requests.get(url, timeout=10)
                    if resp.status_code == 200:
                        data = resp.json()
                        if 'extract' in data:
                            st.success("📖 Wikipedia Summary:")
                            st.write(data['extract'])
                            if 'content_urls' in data:
                                st.markdown(f"[Read more on Wikipedia]({data['content_urls']['desktop']['page']})")
                        else:
                            st.warning("No summary found for this topic.")
                    else:
                        st.error("Could not fetch Wikipedia data.")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    
    # Translation Tool
    st.markdown("""
    <h4>🌐 Translation Tool</h4>
    <span style='font-size:1.1em;'>Translate text between languages using LibreTranslate.</span>
    """, unsafe_allow_html=True)
    
    translate_text = st.text_area("Enter text to translate:", key="translate_text")
    col1, col2 = st.columns(2)
    with col1:
        from_lang = st.selectbox("From:", ["en", "es", "fr", "de", "it", "pt"], key="from_lang")
    with col2:
        to_lang = st.selectbox("To:", ["es", "en", "fr", "de", "it", "pt"], key="to_lang")
    
    if st.button("🔄 Translate", key="translate_btn") and translate_text.strip():
        warning = moderate_content(translate_text, "translation text")
        if warning:
            st.warning(warning)
        else:
            with st.spinner("Translating..."):
                try:
                    resp = requests.post("https://libretranslate.de/translate", json={
                        "q": translate_text,
                        "source": from_lang,
                        "target": to_lang,
                        "format": "text"
                    }, timeout=15)
                    if resp.status_code == 200:
                        result = resp.json()
                        st.success("🔄 Translation:")
                        st.write(result['translatedText'])
                    else:
                        st.error("Translation failed.")
                except Exception as e:
                    st.error(f"Translation error: {e}")

    st.markdown("---")
    
    # Calculator
    st.markdown("""
    <h4>🔢 Calculator</h4>
    <span style='font-size:1.1em;'>Calculate mathematical expressions safely.</span>
    """, unsafe_allow_html=True)
    
    calc_expr = st.text_input("Enter expression (e.g., 2+2*3):", key="calc_expr")
    if st.button("🔢 Calculate", key="calc_btn") and calc_expr.strip():
        try:
            # Safe eval with limited scope
            result = eval(calc_expr, {"__builtins__": None}, {})
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Calculation error: {e}")

with tab3:
    st.markdown("### 🎨 Create & Explore")
    
    # File Upload & Analysis
    st.markdown("""
    <h4>📄 File Upload & Analysis</h4>
    <span style='font-size:1.1em;'>Upload a text file for basic analysis.</span>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a text file", type=["txt"], key="file_upload")
    if uploaded_file is not None:
        try:
            content = str(uploaded_file.read(), "utf-8")
            warning = moderate_content(content, "uploaded file")
            if warning:
                st.warning(warning)
            else:
                st.success("📄 File Analysis:")
                st.write(f"**Word count:** {len(content.split())}")
                st.write(f"**Character count:** {len(content)}")
                st.write(f"**Line count:** {len(content.splitlines())}")
                
                if len(content) > 500:
                    st.write("**Preview (first 500 characters):**")
                    st.text(content[:500] + "...")
                else:
                    st.write("**Full content:**")
                    st.text(content)
        except Exception as e:
            st.error(f"File processing error: {e}")

    st.markdown("---")

    # --- Yantra Pattern Generator Integration ---
    st.markdown("<h4>🕉️ Yantra Pattern Generator</h4>", unsafe_allow_html=True)
    st.write("Generate a yantra (geometric pattern) from any text, mantra, or thought.")
    import importlib.util, os
    mantra_path = os.path.join(os.path.dirname(__file__), 'mantra_yantra', 'mantra_to_yantra.py')
    spec = importlib.util.spec_from_file_location("mantra_to_yantra", mantra_path)
    mantra_yantra = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mantra_yantra)
    yantra_text = st.text_area("Enter text/mantra/thought for yantra:", "Om Mani Padme Hum", key="yantra_text")
    if st.button("Generate Yantra Pattern", key="yantra_btn"):
        try:
            pattern = mantra_yantra.convert_text_to_yantra(yantra_text)
            import matplotlib.pyplot as plt
            import io
            buf = io.BytesIO()
            fig, ax = plt.subplots(figsize=(6,6))
            ax.imshow(pattern)
            ax.axis('off')
            plt.tight_layout()
            fig.savefig(buf, format='png')
            st.image(buf, caption="Yantra Pattern", use_column_width=True)
            plt.close(fig)
        except Exception as e:
            st.error(f"Failed to generate yantra: {e}")
    
    # Text to Speech (placeholder)
    st.markdown("""
    <h4>🔊 Text to Speech</h4>
    <span style='font-size:1.1em;'>Convert text to speech (placeholder - will integrate with TTS service).</span>
    """, unsafe_allow_html=True)
    
    tts_text = st.text_area("Enter text for speech:", key="tts_text")
    if st.button("🔊 Generate Speech", key="tts_btn") and tts_text.strip():
        warning = moderate_content(tts_text, "speech text")
        if warning:
            st.warning(warning)
        else:
            st.info("🔊 TTS feature coming soon! Text ready for speech synthesis.")

with tab4:
    st.markdown("### 🚀 Roadmap & Collaboration")
    
    st.markdown("""
    <div style='background:#f8f9fa;padding:1.5em;border-radius:10px;border-left:4px solid #007bff;'>
        <h4>🚀 Feature Roadmap</h4>
        <p>PB2S is a living, collaborative project. Here are upcoming features you can help shape:</p>
        <ul>
            <li>🧠 <b>Conversational Memory & Context</b>: Smarter, context-aware chat sessions</li>
            <li>🎤 <b>Voice Input (Speech-to-Text)</b>: Talk to PB2S using your voice</li>
            <li>📄 <b>Advanced File Analysis</b>: PDF, DOCX, and code file support</li>
            <li>💻 <b>Code Generation & Execution</b>: Run Python code safely in sandbox</li>
            <li>📚 <b>Personal Knowledge Base</b>: Add your own facts and documents</li>
            <li>🖼️ <b>Multi-modal AI</b>: Image analysis and generation</li>
            <li>🔌 <b>Plugin System</b>: Add custom APIs and tools</li>
            <li>🌍 <b>Accessibility Features</b>: Screen reader support, high contrast</li>
            <li>🔎 <b>Enhanced Transparency</b>: See PB2S reasoning in real-time</li>
            <li>🤝 <b>Community Features</b>: Share prompts and responses</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💬 Your Feedback")
    user_feedback = st.text_area("Share your ideas, vote on features, or report issues:", key="user_feedback_tab4")
    if st.button("📤 Submit Feedback", key="feedback_btn_tab4") and user_feedback.strip():
        st.success("✅ Thank you for your feedback! Your ideas help shape PB2S for everyone.")
    
    st.markdown("---")
    
    st.markdown("""
    <div style='background:#e8f5e8;padding:1em;border-radius:8px;'>
        <h4>🔍 About PB2S</h4>
        <p><b>PB2S (Prompt-Based Self-Alignment System)</b> is an advanced AI framework that uses structured self-reflection:</p>
        <ul>
            <li><b>DRAFT</b>: Generate initial response</li>
            <li><b>REFLECT</b>: Identify contradictions and gaps</li>
            <li><b>REVISE</b>: Improve based on reflection</li>
            <li><b>LEARNED</b>: Extract insights for future use</li>
        </ul>
        <p>This ensures more reliable, thoughtful, and transparent AI responses.</p>
    </div>
    """, unsafe_allow_html=True)