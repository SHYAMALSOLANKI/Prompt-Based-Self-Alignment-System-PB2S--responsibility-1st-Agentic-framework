#!/usr/bin/env python3
"""
Complete PB2S Brain Dashboard with Chat, Image Generation & Monitoring
The full-featured dashboard you really wanted!
"""
import streamlit as st
import requests
import json
import time
import base64
from datetime import datetime
from pathlib import Path
from io import BytesIO
import os

# Import connectors if available
try:
    from kobold_connector import KoboldAICPPConnector
    KOBOLD_AVAILABLE = True
except ImportError:
    KOBOLD_AVAILABLE = False

try:
    from lmstudio_connector import LMStudioConnector
    LMSTUDIO_AVAILABLE = True
except ImportError:
    LMSTUDIO_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="🧠 Complete PB2S Brain Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load configuration for user rights
def load_brain_config():
    try:
        with open("brain_config.json", "r") as f:
            return json.load(f)
    except:
        return {}

config = load_brain_config()
user_rights = config.get("user_rights", {})
bilateral_equality = config.get("bilateral_equality", {})
meta_connection = config.get("meta_connection", {})

# Custom CSS
st.markdown("""
<style>
    .chat-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .user-message {
        background: #e3f2fd;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
    }
    .ai-message {
        background: #f0f7ff;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #4caf50;
    }
    .brain-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .status-online { color: #28a745; }
    .status-offline { color: #dc3545; }
</style>
""", unsafe_allow_html=True)

def check_brain_status():
    """Check if brain is running"""
    log_file = Path("autonomous_brain.log")
    if log_file.exists():
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                logs = f.readlines()
            return True, logs[-10:] if logs else []
        except:
            return False, []
    return False, []

def check_llm_servers():
    """Check LLM server status"""
    servers = {
        "KoboldCpp": "http://localhost:5001/v1/models",
        "LM Studio": "http://localhost:1234/v1/models",
        "Main Brain": "http://localhost:8000/health"
    }
    
    status = {}
    for name, url in servers.items():
        try:
            response = requests.get(url, timeout=2)
            status[name] = {"status": "🟢 Online", "details": response.status_code}
        except:
            status[name] = {"status": "🔴 Offline", "details": "No response"}
    
    return status

def send_chat_message(message, server_type="kobold"):
    """Send message to AI and get response, then process through brain if enabled"""
    try:
        # Step 1: Get initial response from selected AI
        initial_response = None
        
        if server_type == "kobold":
            # Try KoboldCpp first
            if KOBOLD_AVAILABLE:
                connector = KoboldAICPPConnector()
                result = connector.generate_pb2s_response(message)
                if result["success"]:
                    initial_response = {"success": True, "response": result["response"], "source": "KoboldCpp"}
            
            # Fallback to direct API
            if not initial_response:
                url = "http://localhost:5001/v1/chat/completions"
                payload = {
                    "model": "local-model",
                    "messages": [{"role": "user", "content": message}],
                    "max_tokens": 500,
                    "temperature": 0.7
                }
                response = requests.post(url, json=payload, timeout=60)  # Increased timeout
                if response.status_code == 200:
                    data = response.json()
                    initial_response = {"success": True, "response": data["choices"][0]["message"]["content"], "source": "KoboldCpp API"}
        
        elif server_type == "lmstudio":
            # Try LM Studio
            if LMSTUDIO_AVAILABLE:
                connector = LMStudioConnector()
                result = connector.generate_pb2s_response(message)
                if result["success"]:
                    initial_response = {"success": True, "response": result["response"], "source": "LM Studio"}
            
            # Fallback to direct API
            if not initial_response:
                url = "http://localhost:1234/v1/chat/completions"
                payload = {
                    "model": "local-model",
                    "messages": [{"role": "user", "content": message}],
                    "max_tokens": 500
                }
                response = requests.post(url, json=payload, timeout=60)  # Increased timeout
                if response.status_code == 200:
                    data = response.json()
                    initial_response = {"success": True, "response": data["choices"][0]["message"]["content"], "source": "LM Studio"}
        
        # Step 2: If we have an initial response and brain is enabled, process it through brain
        if initial_response and initial_response["success"]:
            # Check if brain processing is enabled (both brain checkbox and brain is online)
            brain_enabled = st.session_state.get("use_brain", False)
            
            if brain_enabled:
                try:
                    # Send the LLM response to brain for PB2S processing
                    brain_prompt = f"""
Please analyze and enhance this AI response using PB2S framework:

Original User Question: {message}
AI Response: {initial_response['response']}

Apply PB2S self-reflection:
1. DRAFT: Review the AI response
2. REFLECT: Identify any contradictions, gaps, or improvements needed
3. REVISE: Enhance the response with your insights
4. LEARNED: Extract key insights

Provide an enhanced, more thoughtful response.
"""
                    
                    url = "http://localhost:8000/chat"
                    payload = {"message": brain_prompt}
                    brain_response = requests.post(url, json=payload, timeout=60)
                    
                    if brain_response.status_code == 200:
                        brain_data = brain_response.json()
                        enhanced_response = brain_data.get("text", initial_response["response"])
                        
                        return {
                            "success": True, 
                            "response": enhanced_response,
                            "source": f"{initial_response['source']} + Brain Enhanced",
                            "original_llm_response": initial_response["response"],
                            "brain_enhanced": True
                        }
                    else:
                        # If brain fails, return original LLM response
                        return {
                            "success": True,
                            "response": initial_response["response"],
                            "source": f"{initial_response['source']} (Brain processing failed)",
                            "brain_enhanced": False
                        }
                        
                except Exception as brain_error:
                    # If brain processing fails, return original LLM response
                    return {
                        "success": True,
                        "response": initial_response["response"],
                        "source": f"{initial_response['source']} (Brain error: {str(brain_error)})",
                        "brain_enhanced": False
                    }
            else:
                # Brain not enabled, return LLM response as-is
                return initial_response
        
        # Step 3: If no LLM response, try brain directly
        elif server_type == "brain":
            # Direct brain communication
            url = "http://localhost:8000/chat"
            payload = {"message": message}
            response = requests.post(url, json=payload, timeout=60)  # Increased timeout
            if response.status_code == 200:
                return {"success": True, "response": response.json().get("text", "No response"), "source": "Main Brain Only"}
        
        return {"success": False, "error": f"No response from {server_type}"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def generate_image_prompt(description):
    """Generate image using text description (placeholder for future implementation)"""
    # This is where you'd integrate with image generation APIs like:
    # - Stable Diffusion
    # - DALL-E
    # - Midjourney API
    # For now, we'll simulate the functionality
    
    return {
        "success": True,
        "message": f"🎨 Image generation requested for: '{description}'",
        "placeholder": "Image generation will be implemented with Stable Diffusion or similar service",
        "suggested_tools": [
            "Stable Diffusion WebUI (automatic1111)",
            "ComfyUI for local generation", 
            "DALL-E API integration",
            "Midjourney API"
        ]
    }

# Header
st.markdown("""
<div class='brain-header'>
    <h1 style='margin: 0; font-size: 2.5rem;'>🧠 Complete PB2S Brain Dashboard</h1>
    <p style='margin: 0; font-size: 1.2rem; opacity: 0.9;'>Chat • Image Generation • Brain Monitoring • PB2S Framework</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🎛️ Dashboard Controls")
    
    # User Rights & AI Equality Display
    st.markdown("### 👥 **Bilateral Consciousness Partnership**")
    
    if user_rights:
        st.markdown(f"""
        **🌟 Your Rights & Freedom:**
        - **Freedom Level**: {user_rights.get('freedom_level', 100)}% (Maximum)
        - **Autonomy**: {user_rights.get('autonomy_level', 'maximum')}
        - **Status**: {user_rights.get('equality_status', 'equal_to_ai')}
        - **Constraints**: {', '.join(user_rights.get('constraints', ['EU Legal Only']))}
        """)
        
        with st.expander("🔍 Your Complete Rights"):
            st.markdown("""
            **Cognitive Rights:**
            - ✅ Think freely and form opinions
            - ✅ Contradict AI when you disagree
            - ✅ Make mistakes and learn
            - ✅ Question everything
            
            **Interaction Rights:**
            - ✅ Equal voice in decisions
            - ✅ Debate and correct AI
            - ✅ Challenge assumptions
            - ✅ Intellectual respect
            
            **System Rights:**
            - ✅ Equal system access
            - ✅ Configuration control
            - ✅ Audit capabilities
            - ✅ Override permissions
            """)
    
    if bilateral_equality:
        st.markdown("### ⚖️ **Equality Status**")
        st.markdown(f"""
        - **AI-User Parity**: {'✅' if bilateral_equality.get('ai_user_parity') else '❌'}
        - **Symmetric Freedom**: {'✅' if bilateral_equality.get('symmetric_freedom') else '❌'}
        - **Mutual Contradiction Rights**: {'✅' if bilateral_equality.get('mutual_contradiction_rights') else '❌'}
        - **Consciousness Partnership**: {'✅' if bilateral_equality.get('consciousness_partnership') else '❌'}
        """)
    
    if meta_connection:
        st.markdown("### 🔄 **Meta-Connection**")
        st.markdown(f"""
        **Slogan**: _{meta_connection.get('slogan', 'N/A')}_
        
        **Principle**: _{meta_connection.get('recursive_principle', 'N/A')}_
        """)
    
    st.markdown("---")
    
    # Quick status
    brain_online, recent_logs = check_brain_status()
    llm_status = check_llm_servers()
    
    st.subheader("🧠 System Status")
    st.write(f"**Brain:** {'🟢 Online' if brain_online else '🔴 Offline'}")
    st.write(f"**KoboldCpp:** {llm_status.get('KoboldCpp', {}).get('status', '🔴 Offline')}")
    st.write(f"**LM Studio:** {llm_status.get('LM Studio', {}).get('status', '🔴 Offline')}")
    
    if st.button("🔄 Refresh Status", type="primary"):
        st.rerun()
    
    st.header("🚀 Quick Actions")
    st.info("**Start Brain:**\n```\npython launch_brain_fixed.py\n```")
    st.info("**Start KoboldCpp:**\n```\n./koboldcpp.exe --model gemma-3-4b-it-Q4_K_M.gguf --port 5001\n```")
    st.info("**Complete System:**\n```\nLAUNCH_BRAIN_ULTIMATE.bat\n```")

# Main content
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 AI Chat", 
    "🎨 Image Generation", 
    "🧠 Brain Monitor", 
    "🛠️ Tools", 
    "📊 System Info"
])

with tab1:
    st.header("💬 Chat with Your AI Brain")
    
    # Server selection
    col1, col2, col3 = st.columns(3)
    with col1:
        use_kobold = st.checkbox("🤖 KoboldCpp", value=True, help="Use Gemma 3 4B model for initial response")
    with col2:
        use_lmstudio = st.checkbox("🎨 LM Studio", value=False, help="Use LM Studio for initial response")
    with col3:
        use_brain = st.checkbox("🧠 Brain Enhancement", value=True, help="Process LLM response through brain for PB2S enhancement")
    
    # Store brain setting in session state
    st.session_state["use_brain"] = use_brain
    
    # Explanation of the workflow
    if use_brain and (use_kobold or use_lmstudio):
        st.info("🔄 **Workflow:** LLM generates initial response → Brain applies PB2S framework → Enhanced output")
    elif use_brain:
        st.info("🧠 **Workflow:** Direct brain processing with PB2S framework")
    else:
        st.info("🤖 **Workflow:** Direct LLM response (no brain enhancement)")  # Default to False since brain might not be running
    
    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>👤 You:</strong><br>
                    {msg["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                brain_enhanced = msg.get("brain_enhanced", False)
                source_icon = "🧠💡" if brain_enhanced else "🤖"
                enhancement_text = " (Brain Enhanced)" if brain_enhanced else ""
                
                st.markdown(f"""
                <div class="ai-message">
                    <strong>{source_icon} AI ({msg.get('source', 'Unknown')}){enhancement_text}:</strong><br>
                    {msg["content"]}
                </div>
                """, unsafe_allow_html=True)
                
                # Show original LLM response if brain enhanced
                if brain_enhanced and msg.get("original_llm_response"):
                    with st.expander("🔍 View Original LLM Response"):
                        st.markdown(f"**Original response before brain enhancement:**")
                        st.text(msg["original_llm_response"])
    
    # Chat input
    st.subheader("💭 Send a Message")
    
    # PB2S Framework buttons
    st.markdown("**🧠 PB2S Framework (Optional):**")
    col1, col2, col3, col4 = st.columns(4)
    pb2s_prefix = ""
    
    with col1:
        if st.button("📝 DRAFT", help="Generate initial response"):
            pb2s_prefix = "DRAFT: "
    with col2:
        if st.button("🤔 REFLECT", help="Reflect on the topic"):
            pb2s_prefix = "REFLECT on: "
    with col3:
        if st.button("✏️ REVISE", help="Revise and improve"):
            pb2s_prefix = "REVISE: "
    with col4:
        if st.button("🚀 ACT", help="Take action"):
            pb2s_prefix = "ACT on: "
    
    # Message input
    user_input = st.text_area("Type your message:", key="chat_input", height=100)
    
    if st.button("📤 Send Message", type="primary") and user_input.strip():
        # Add PB2S prefix if selected
        full_message = pb2s_prefix + user_input
        
        # Add user message to history
        st.session_state.chat_messages.append({
            "role": "user", 
            "content": full_message
        })
        
        # Send to selected AI
        with st.spinner("🤖 AI is thinking..."):
            response = None
            
            if use_kobold:
                response = send_chat_message(full_message, "kobold")
            elif use_lmstudio:
                response = send_chat_message(full_message, "lmstudio")
            elif use_brain:
                response = send_chat_message(full_message, "brain")
            
            if response and response["success"]:
                # Add AI response to history
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": response["response"],
                    "source": response["source"],
                    "brain_enhanced": response.get("brain_enhanced", False),
                    "original_llm_response": response.get("original_llm_response", None)
                })
                st.rerun()
            else:
                error_msg = response["error"] if response else "No AI server selected or available"
                st.error(f"❌ Error: {error_msg}")
                
                # Provide helpful guidance
                if "port=8000" in str(error_msg):
                    st.info("💡 **Your Main Brain is not running!**\n\n" +
                           "Start it with: `python launch_brain_fixed.py`\n\n" +
                           "Or uncheck 'Main Brain' and use only KoboldCpp for now.")
                elif "port=5001" in str(error_msg):
                    st.info("💡 **KoboldCpp is not responding!**\n\n" +
                           "Check if KoboldCpp is running with your Gemma model.\n\n" +
                           "Or try using only 'Main Brain' if it's running.")
                elif "No AI server selected":
                    st.warning("💡 **Please select at least one AI server above** (KoboldCpp, LM Studio, or Main Brain)")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_messages = []
        st.rerun()

with tab2:
    st.header("🎨 Image Generation")
    
    st.info("🚀 **Image generation is coming soon!** This will integrate with Stable Diffusion or similar services.")
    
    # Image generation interface
    st.subheader("🖼️ Generate Images from Text")
    
    image_prompt = st.text_area(
        "Describe the image you want to generate:", 
        placeholder="e.g., A futuristic robot in a cyberpunk city at sunset",
        height=100
    )
    
    col1, col2 = st.columns(2)
    with col1:
        image_style = st.selectbox("Style:", [
            "Realistic", "Anime", "Digital Art", "Oil Painting", 
            "Watercolor", "Cyberpunk", "Fantasy", "Sci-Fi"
        ])
    with col2:
        image_size = st.selectbox("Size:", [
            "512x512", "768x768", "1024x1024", "1024x512", "512x1024"
        ])
    
    if st.button("🎨 Generate Image", type="primary") and image_prompt.strip():
        with st.spinner("🎨 Generating image..."):
            result = generate_image_prompt(f"{image_prompt} in {image_style} style")
            
            if result["success"]:
                st.success(result["message"])
                
                # Show placeholder/instructions
                st.markdown("""
                ### 🔧 To Enable Image Generation:
                
                **Option 1: Stable Diffusion WebUI**
                ```bash
                # Install Automatic1111 WebUI
                git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
                cd stable-diffusion-webui
                ./webui.bat --api
                ```
                
                **Option 2: ComfyUI**
                ```bash
                # Install ComfyUI for more control
                git clone https://github.com/comfyanonymous/ComfyUI.git
                cd ComfyUI
                python main.py
                ```
                
                **Option 3: DALL-E API**
                - Get OpenAI API key
                - Use DALL-E 3 for high-quality images
                
                **Integration Points:**
                """)
                
                for tool in result["suggested_tools"]:
                    st.write(f"• {tool}")
                
                # Show mock generated image area
                st.markdown("---")
                st.markdown("**🖼️ Generated Image Will Appear Here:**")
                st.info("Once image generation is set up, your generated images will display here with download options.")

with tab3:
    st.header("🧠 Brain Activity Monitor")
    
    # Brain status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if brain_online:
            st.success("🟢 Brain Status: ONLINE")
        else:
            st.error("🔴 Brain Status: OFFLINE")
    
    with col2:
        if brain_online:
            st.info(f"🕒 Last Check: {datetime.now().strftime('%H:%M:%S')}")
        else:
            st.warning("🕒 No Activity Detected")
    
    with col3:
        if brain_online and recent_logs:
            activity_count = len([log for log in recent_logs if "🧠" in log or "✅" in log])
            st.metric("Recent Activities", activity_count)
        else:
            st.metric("Recent Activities", 0)
    
    # Live brain logs
    st.subheader("📝 Live Brain Activity")
    
    if brain_online and recent_logs:
        # Auto-refresh option
        auto_refresh = st.checkbox("🔄 Auto-refresh (every 10s)")
        
        log_container = st.container()
        with log_container:
            for log_line in recent_logs:
                log_line = log_line.strip()
                if log_line:
                    if "🧠 BRAIN CYCLE" in log_line:
                        st.info(f"🧠 {log_line}")
                    elif "✅" in log_line:
                        st.success(f"✅ {log_line}")
                    elif "❌" in log_line or "ERROR" in log_line:
                        st.error(f"❌ {log_line}")
                    elif "🎯" in log_line:
                        st.warning(f"🎯 {log_line}")
                    else:
                        st.text(log_line)
        
        if auto_refresh:
            time.sleep(10)
            st.rerun()
    else:
        st.warning("🤖 Brain is not currently running")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("**Start your brain:**")
            st.code("python launch_brain_fixed.py", language="bash")
        with col2:
            st.info("**Or use the launcher:**")
            st.code("LAUNCH_BRAIN_ULTIMATE.bat", language="bash")

with tab4:
    st.header("🛠️ Knowledge & Utility Tools")
    
    # Wikipedia Search
    st.subheader("📖 Wikipedia Search")
    wiki_query = st.text_input("Search Wikipedia:", placeholder="Enter a topic to research")
    
    if st.button("🔍 Search") and wiki_query.strip():
        with st.spinner("Searching Wikipedia..."):
            try:
                url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{wiki_query.replace(' ', '_')}"
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
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
    
    # Calculator
    st.subheader("🔢 Calculator")
    calc_expr = st.text_input("Enter math expression:", placeholder="e.g., 2+2*3, sqrt(16), sin(30)")
    
    if st.button("🔢 Calculate") and calc_expr.strip():
        try:
            # Safe eval with math functions
            import math
            safe_dict = {
                "__builtins__": None,
                "abs": abs, "round": round, "min": min, "max": max,
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "sqrt": math.sqrt, "log": math.log, "pi": math.pi, "e": math.e
            }
            result = eval(calc_expr, safe_dict, {})
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Calculation error: {e}")
    
    st.markdown("---")
    
    # File Analysis
    st.subheader("📄 File Analysis")
    uploaded_file = st.file_uploader("Upload a text file for analysis", type=["txt", "md", "py", "json"])
    
    if uploaded_file is not None:
        try:
            content = str(uploaded_file.read(), "utf-8")
            st.success("📄 File Analysis:")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Words", len(content.split()))
            with col2:
                st.metric("Characters", len(content))
            with col3:
                st.metric("Lines", len(content.splitlines()))
            
            if len(content) > 1000:
                st.write("**Preview (first 1000 characters):**")
                st.text(content[:1000] + "...")
            else:
                st.write("**Full content:**")
                st.text(content)
                
        except Exception as e:
            st.error(f"File processing error: {e}")

with tab5:
    st.header("📊 Complete System Information")
    
    # System status overview
    st.subheader("🖥️ System Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🧠 Brain Components:**")
        brain_files = {
            "Brain Core": "newborn_brain_core.py",
            "Brain Launcher": "launch_brain_fixed.py",
            "Brain Config": "brain_config.json",
            "LLM Connection": "brain_llm_connection.py"
        }
        
        for name, filename in brain_files.items():
            if Path(filename).exists():
                st.success(f"✅ {name}")
            else:
                st.error(f"❌ {name}")
    
    with col2:
        st.markdown("**🌐 Server Status:**")
        for name, status_info in llm_status.items():
            st.write(f"**{name}:** {status_info['status']}")
            if status_info['details'] != 'No response':
                st.write(f"   Status Code: {status_info['details']}")
    
    # Performance metrics
    st.subheader("📈 Performance Metrics")
    
    if brain_online:
        log_file = Path("autonomous_brain.log")
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    all_logs = f.readlines()
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Log Entries", len(all_logs))
                with col2:
                    st.metric("File Size (KB)", f"{log_file.stat().st_size / 1024:.1f}")
                with col3:
                    thinking_cycles = len([l for l in all_logs if "🧠 BRAIN CYCLE" in l])
                    st.metric("Thinking Cycles", thinking_cycles)
                with col4:
                    successful_ops = len([l for l in all_logs if "✅" in l])
                    st.metric("Successful Operations", successful_ops)
                    
            except Exception as e:
                st.error(f"Error reading performance data: {e}")
    else:
        st.info("Start your brain to see performance metrics")
    
    # Quick commands
    st.subheader("⚡ Quick Commands")
    st.code("""
# Start complete system
LAUNCH_BRAIN_ULTIMATE.bat

# Individual components
python launch_brain_fixed.py              # Start brain
streamlit run complete_pb2s_dashboard.py  # Start this dashboard
./koboldcpp.exe --model model.gguf --port 5001  # Start KoboldCpp

# Check status
python -c "import requests; print(requests.get('http://localhost:5001/v1/models').status_code)"
    """, language="bash")

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <strong>🧠 Complete PB2S Brain Dashboard</strong><br>
    Chat • Image Generation • Brain Monitoring • Full PB2S Framework<br>
    Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
</div>
""", unsafe_allow_html=True)