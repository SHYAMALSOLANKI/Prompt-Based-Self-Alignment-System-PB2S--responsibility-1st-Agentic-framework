#!/usr/bin/env python3
"""
PB2S Lightweight Dashboard - Optimized for Low-Resource Systems
============================================================

This is a lightweight version of the PB2S dashboard designed for:
- Older hardware (like i5 Core M with 8GB RAM)
- Development and testing without local LLMs
- API-only mode focusing on PB2S structure
- Preparation for Jetson Orin deployment

Author: PB2S Framework Team
Date: 2025-01-23
Hardware Target: Development systems without GPU/high RAM
"""

import streamlit as st
import requests
import json
import time
import sys
from pathlib import Path

# Streamlit Configuration
st.set_page_config(
    page_title="PB2S Lightweight Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def check_system_resources():
    """Display system resource information"""
    import psutil
    
    st.sidebar.header("💻 System Resources")
    
    # CPU info
    cpu_percent = psutil.cpu_percent(interval=1)
    st.sidebar.metric("CPU Usage", f"{cpu_percent}%")
    
    # Memory info
    memory = psutil.virtual_memory()
    memory_gb = memory.total / (1024**3)
    memory_used_percent = memory.percent
    st.sidebar.metric("RAM Total", f"{memory_gb:.1f} GB")
    st.sidebar.metric("RAM Usage", f"{memory_used_percent}%")
    
    # Resource recommendations
    if memory_gb < 16:
        st.sidebar.warning("⚠️ Low RAM detected. Local LLMs not recommended.")
        st.sidebar.info("💡 Use API-only mode or deploy to Jetson Orin")
    
    if cpu_percent > 80:
        st.sidebar.error("🔥 High CPU usage detected")

def main():
    """Main dashboard function - lightweight version"""
    
    # Header
    st.title("🧠 PB2S Lightweight Dashboard")
    st.markdown("**Prompt-Based Self-Alignment System** - Development Mode")
    
    # System resources in sidebar
    check_system_resources()
    
    # Configuration section
    st.sidebar.header("⚙️ Configuration")
    mode = st.sidebar.selectbox(
        "Dashboard Mode",
        ["API Only (Lightweight)", "Jetson Ready (Preview)"],
        help="API Only mode for current laptop, Jetson Ready for when hardware arrives"
    )
    
    if mode == "API Only (Lightweight)":
        show_api_only_dashboard()
    else:
        show_jetson_preview_dashboard()

def show_api_only_dashboard():
    """Show API-only dashboard for lightweight systems"""
    
    st.header("🎯 API-Only Mode")
    st.info("💡 Perfect for development on low-resource systems. Local LLMs will run on Jetson Orin.")
    
    # Single node configuration
    node = {
        "name": "Main Brain", 
        "url": "http://127.0.0.1:8000", 
        "role": "🎯 Main reasoning and conversation",
        "type": "api"
    }
    
    # Node status
    st.markdown(f"### 🧠 {node['name']}")
    st.markdown(f"**Role**: {node['role']}")
    
    # Status check
    try:
        resp = requests.get(node["url"] + "/chat", timeout=2)
        st.success(f"✅ {node['name']} is online and ready at {node['url']}")
        server_online = True
    except Exception as e:
        st.error(f"❌ {node['name']} at {node['url']} is offline")
        st.info("💡 Start the main brain with: python pb2s_enhanced_server.py")
        server_online = False
    
    # Chat interface
    st.markdown("### 💬 Chat Interface")
    
    # PB2S Structure buttons
    st.markdown("**PB2S Structure Templates:**")
    col1, col2, col3, col4 = st.columns(4)
    
    prompt_template = ""
    with col1:
        if st.button("📝 DRAFT", help="Initial response draft"):
            prompt_template = "[DRAFT] "
    with col2:
        if st.button("🤔 REFLECT", help="Reflect on previous response"):
            prompt_template = "[REFLECT] "
    with col3:
        if st.button("✏️ REVISE", help="Revise based on reflection"):
            prompt_template = "[REVISE] "
    with col4:
        if st.button("🎓 LEARNED", help="Extract key learning"):
            prompt_template = "[LEARNED] "
    
    # Chat input
    user_input = st.text_area(
        "Your message:",
        value=prompt_template,
        height=100,
        help="Enter your message. Use PB2S structure tags for better responses."
    )
    
    # Send button
    if st.button("🚀 Send Message", disabled=not server_online):
        if user_input.strip():
            with st.spinner("🧠 Processing..."):
                try:
                    # Send to main brain
                    response = requests.post(
                        node["url"] + "/chat",
                        json={"message": user_input},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        ai_reply = response.json()
                        
                        # Display response
                        st.markdown("### 🤖 Response:")
                        response_text = ai_reply.get('text', str(ai_reply))
                        
                        st.markdown(f"""
<div style='background:#f0f7ff;padding:1em 1.2em;border-radius:1em;box-shadow:0 1px 4px #e0e0e0;margin:1em 0;'>
    <b style='color:#1a1a1a;'>🧠 Main Brain:</b><br>
    <span style='color:#222;font-size:1.1em;line-height:1.5;'>{response_text}</span>
</div>
""", unsafe_allow_html=True)
                        
                        # Show PB2S proof if available
                        if 'pb2s_proof' in ai_reply:
                            with st.expander("🔍 PB2S Self-Reflection Details"):
                                st.json(ai_reply['pb2s_proof'])
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                        
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
        else:
            st.warning("Please enter a message")

def show_jetson_preview_dashboard():
    """Show preview of what dashboard will look like on Jetson Orin"""
    
    st.header("🚀 Jetson Orin Preview Mode")
    st.success("✨ Preview of capabilities when deployed to Jetson Orin with 1TB NVMe storage")
    
    # Future node configuration
    jetson_nodes = [
        {"name": "Main Brain", "status": "✅ Ready", "specs": "FastAPI Server"},
        {"name": "TinyLlama 1.1B", "status": "🎯 Optimized", "specs": "700MB, Q4_K_M, 300-word vocab"},
        {"name": "Phi-2 2.7B", "status": "🎯 Optimized", "specs": "1.6GB, Q4_K_M, Reasoning focus"},
        {"name": "StableLM 3B", "status": "🎯 Optimized", "specs": "1.9GB, Q4_K_M, Instruction tuned"},
        {"name": "Mistral 7B", "status": "🎯 Optional", "specs": "4.37GB, Q4_K_M, Full capability"}
    ]
    
    st.markdown("### 🤖 Planned Local Models for Jetson Orin:")
    
    for node in jetson_nodes:
        col1, col2, col3 = st.columns([3, 2, 4])
        with col1:
            st.markdown(f"**{node['name']}**")
        with col2:
            st.markdown(node['status'])
        with col3:
            st.markdown(f"`{node['specs']}`")
    
    # Jetson specifications
    st.markdown("### 📊 Jetson Orin Specifications:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
**Hardware:**
- 🧠 ARM Cortex-A78AE CPU
- 🎮 NVIDIA Ampere GPU
- 💾 8GB LPDDR5 RAM
- 💽 1TB NVMe PCIe 4.0 SSD
        """)
    
    with col2:
        st.markdown("""
**AI Capabilities:**
- 🚀 40 TOPS AI Performance
- 🔥 CUDA Acceleration
- ⚡ TensorRT Optimization
- 🔧 ONNX Support
        """)
    
    # Sustainability metrics
    st.markdown("### 🌱 Sustainability Metrics:")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Power Consumption", "15-20W", "vs 300W+ Desktop")
    with col2:
        st.metric("Carbon Footprint", "Low", "Edge computing")
    with col3:
        st.metric("Efficiency", "High", "TOPS/Watt optimized")
    
    # Deployment timeline
    st.markdown("### 📅 Deployment Roadmap:")
    st.markdown("""
1. **Phase 1**: Setup Jetson Orin with Ubuntu
2. **Phase 2**: Install Docker and NVIDIA Container Runtime
3. **Phase 3**: Deploy PB2S with optimized models
4. **Phase 4**: Configure 1TB NVMe for model storage
5. **Phase 5**: Enable Google Drive sync for learning data
6. **Phase 6**: Production deployment with monitoring
    """)

# Add resource monitoring
def show_resource_monitor():
    """Show system resource monitoring"""
    st.sidebar.header("📊 Resource Monitor")
    
    # Placeholder for real-time metrics
    if st.sidebar.button("🔄 Refresh"):
        st.rerun()

if __name__ == "__main__":
    try:
        # Add resource monitoring
        show_resource_monitor()
        
        # Run main dashboard
        main()
        
        # Footer
        st.markdown("---")
        st.markdown("**PB2S Framework** - Lightweight Dashboard v1.0 | Ready for Jetson Orin deployment")
        
    except Exception as e:
        st.error(f"Dashboard error: {str(e)}")
        st.info("Please ensure all dependencies are installed and the main brain server is running.")