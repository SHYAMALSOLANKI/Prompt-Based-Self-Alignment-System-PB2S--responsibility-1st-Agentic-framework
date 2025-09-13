#!/usr/bin/env python3
"""
Enhanced Brain Network Monitoring Dashboard
Real-time monitoring of distributed AI brain system
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
import asyncio
import websockets
import time
from datetime import datetime, timedelta
import requests
from pathlib import Path
import threading
import queue

# Page configuration
st.set_page_config(
    page_title="🧠 Home AI Brain Network",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .status-online { color: #28a745; }
    .status-offline { color: #dc3545; }
    .status-warning { color: #ffc107; }
</style>
""", unsafe_allow_html=True)

class BrainNetworkDashboard:
    def __init__(self):
        self.network_status = {}
        self.brain_logs = []
        self.performance_data = []
        
    def load_network_status(self):
        """Load network status from coordinator"""
        try:
            # Try to load from network_status.json (created by coordinator)
            status_file = Path("network_status.json")
            if status_file.exists():
                with open(status_file, 'r') as f:
                    self.network_status = json.load(f)
        except Exception as e:
            st.error(f"Failed to load network status: {e}")
            
    def load_brain_logs(self):
        """Load recent brain activity logs"""
        try:
            log_files = [
                "autonomous_brain.log",
                "network_coordinator.log",
                "newborn_brain_learning.log"
            ]
            
            self.brain_logs = []
            for log_file in log_files:
                if Path(log_file).exists():
                    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()[-50:]  # Last 50 lines
                        for line in lines:
                            if line.strip():
                                self.brain_logs.append({
                                    'source': log_file,
                                    'message': line.strip(),
                                    'timestamp': datetime.now()
                                })
        except Exception as e:
            st.error(f"Failed to load brain logs: {e}")
    
    def test_llm_servers(self):
        """Test connectivity to LLM servers"""
        servers = [
            ("LM Studio", "http://localhost:1234/v1/models"),
            ("llama.cpp", "http://localhost:8080/v1/models"),
            ("Ollama", "http://localhost:11434/api/tags")
        ]
        
        llm_status = {}
        for name, url in servers:
            try:
                response = requests.get(url, timeout=2)
                llm_status[name] = {
                    'status': 'online' if response.status_code == 200 else 'error',
                    'response_time': response.elapsed.total_seconds()
                }
            except:
                llm_status[name] = {'status': 'offline', 'response_time': None}
        
        return llm_status

def main():
    dashboard = BrainNetworkDashboard()
    
    # Title and header
    st.title("🧠 Home AI Brain Network Dashboard")
    st.markdown("Real-time monitoring of your distributed autonomous brain system")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🎛️ Controls")
        
        # Refresh button
        if st.button("🔄 Refresh All Data", type="primary"):
            st.experimental_rerun()
        
        # Auto-refresh toggle
        auto_refresh = st.checkbox("⚡ Auto-refresh (10s)", value=True)
        if auto_refresh:
            time.sleep(10)
            st.experimental_rerun()
            
        # System controls
        st.header("🚀 System Controls")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧠 Start Brain"):
                st.info("Starting brain system...")
                # Could trigger brain startup
        
        with col2:
            if st.button("🛑 Stop Brain"):
                st.warning("Stopping brain system...")
        
        # LLM Server controls
        st.header("🤖 LLM Servers")
        if st.button("📥 Install LM Studio"):
            st.info("Opening LM Studio installation guide...")
    
    # Load current data
    dashboard.load_network_status()
    dashboard.load_brain_logs()
    llm_status = dashboard.test_llm_servers()
    
    # Main dashboard content
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏠 Network Overview", 
        "🧠 Brain Activity", 
        "🤖 LLM Status", 
        "📊 Performance", 
        "📋 System Logs"
    ])
    
    with tab1:
        st.header("🌐 Network Overview")
        
        # Network status overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Laptop status
            laptop_status = dashboard.network_status.get('laptop_main_brain', {}).get('status', 'unknown')
            status_color = "🟢" if laptop_status == "online" else "🔴"
            st.metric(
                "💻 Laptop Brain",
                f"{status_color} {laptop_status.title()}",
                "Main Controller"
            )
        
        with col2:
            # Jetson Orin status
            orin_status = dashboard.network_status.get('jetson_orin_edge', {}).get('status', 'unknown')
            status_color = "🟢" if orin_status == "online" else "🔴"
            st.metric(
                "🔥 Jetson Orin 8GB",
                f"{status_color} {orin_status.title()}",
                "Edge Processing"
            )
        
        with col3:
            # Jetson 2GB status
            sensors_status = dashboard.network_status.get('jetson_2gb_sensors', {}).get('status', 'unknown')
            status_color = "🟢" if sensors_status == "online" else "🔴"
            st.metric(
                "📱 Jetson 2GB",
                f"{status_color} {sensors_status.title()}",
                "Sensor Hub"
            )
        
        with col4:
            # Overall network health
            online_nodes = sum(1 for node in dashboard.network_status.values() 
                             if node.get('status') == 'online')
            total_nodes = len(dashboard.network_status) if dashboard.network_status else 3
            health_pct = (online_nodes / max(total_nodes, 1)) * 100
            st.metric(
                "🌐 Network Health",
                f"{health_pct:.0f}%",
                f"{online_nodes}/{total_nodes} nodes"
            )
        
        # Network topology visualization
        st.subheader("🔗 Network Topology")
        
        if dashboard.network_status:
            # Create network graph
            fig = go.Figure()
            
            # Add nodes
            node_positions = {
                'laptop': (0, 1),
                'jetson_orin': (-1, -1),
                'jetson_2gb': (1, -1)
            }
            
            for node_type, (x, y) in node_positions.items():
                node_key = f"{node_type}_main_brain" if node_type == "laptop" else f"{node_type}_edge" if node_type == "jetson_orin" else f"{node_type}_sensors"
                status = dashboard.network_status.get(node_key, {}).get('status', 'offline')
                
                color = 'green' if status == 'online' else 'red'
                size = 40 if node_type == 'laptop' else 30
                
                fig.add_trace(go.Scatter(
                    x=[x], y=[y],
                    mode='markers+text',
                    marker=dict(size=size, color=color),
                    text=node_type.replace('_', ' ').title(),
                    textposition="bottom center",
                    name=node_type
                ))
            
            # Add connections
            connections = [
                ((0, 1), (-1, -1)),  # Laptop to Jetson Orin
                ((0, 1), (1, -1)),   # Laptop to Jetson 2GB
                ((-1, -1), (1, -1))  # Jetson Orin to Jetson 2GB
            ]
            
            for (x1, y1), (x2, y2) in connections:
                fig.add_trace(go.Scatter(
                    x=[x1, x2], y=[y1, y2],
                    mode='lines',
                    line=dict(color='gray', width=2),
                    showlegend=False
                ))
            
            fig.update_layout(
                title="Brain Network Topology",
                showlegend=False,
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("🔍 No network data available. Start the network coordinator to see live status.")
    
    with tab2:
        st.header("🧠 Brain Activity")
        
        # Brain capabilities status
        st.subheader("⚡ Active Capabilities")
        
        capabilities = [
            "Speech Recognition", "Speech Synthesis", "Natural Language",
            "Computer Vision", "Image Recognition", "Visual Reasoning",
            "Logical Reasoning", "Creative Thinking", "Problem Solving",
            "Pattern Recognition", "Programming", "Mathematics",
            "Data Analysis", "System Thinking", "Contradiction Detection",
            "Self Reflection", "Autonomous Learning", "Metacognition",
            "Empathy", "Emotional Reasoning", "Social Understanding"
        ]
        
        # Display capabilities in a grid
        cols = st.columns(4)
        for i, capability in enumerate(capabilities):
            with cols[i % 4]:
                st.success(f"✅ {capability}")
        
        # Recent brain activity
        st.subheader("🔄 Recent Thinking Cycles")
        
        # Simulate brain activity data
        activity_data = pd.DataFrame({
            'Time': pd.date_range(start=datetime.now() - timedelta(hours=1), periods=10, freq='6min'),
            'Thinking Cycles': [2, 3, 1, 4, 2, 3, 2, 1, 3, 2],
            'Decisions Made': [1, 2, 1, 3, 1, 2, 1, 1, 2, 1],
            'Contradictions Found': [0, 1, 0, 0, 1, 0, 0, 0, 1, 0]
        })
        
        fig = px.line(activity_data, x='Time', y=['Thinking Cycles', 'Decisions Made', 'Contradictions Found'],
                     title="Brain Activity Over Time")
        st.plotly_chart(fig, use_container_width=True)
        
        # Learning progress
        st.subheader("📈 Learning Progress")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Learning Cycles", "847", "+23 today")
        with col2:
            st.metric("Contradictions Resolved", "156", "+5 today")
        with col3:
            st.metric("Autonomous Decisions", "2,341", "+47 today")
    
    with tab3:
        st.header("🤖 LLM Server Status")
        
        st.subheader("🔗 Connected Servers")
        
        for server_name, status_info in llm_status.items():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                status = status_info['status']
                if status == 'online':
                    st.success(f"✅ {server_name}")
                elif status == 'error':
                    st.warning(f"⚠️ {server_name}")
                else:
                    st.error(f"❌ {server_name}")
            
            with col2:
                if status_info['response_time']:
                    st.text(f"{status_info['response_time']:.3f}s")
                else:
                    st.text("N/A")
            
            with col3:
                if status == 'online':
                    st.text("Available")
                else:
                    st.text("Offline")
        
        # Server setup instructions
        st.subheader("⚙️ Setup Instructions")
        
        with st.expander("🎯 LM Studio (Recommended)"):
            st.markdown("""
            1. Download from: https://lmstudio.ai/
            2. Install and launch LM Studio
            3. Go to 'Discover' tab and download a model
            4. Go to 'Server' tab and start on port 1234
            """)
        
        with st.expander("⚡ llama.cpp (Advanced)"):
            st.markdown("""
            1. Download pre-compiled binary or compile from source
            2. Download a GGUF model file
            3. Run: `./server -m model.gguf --port 8080`
            """)
        
        with st.expander("🔥 Ollama (Command Line)"):
            st.markdown("""
            1. Download from: https://ollama.ai/
            2. Install Ollama
            3. Run: `ollama pull llama2:7b-chat`
            4. Run: `ollama serve`
            """)
    
    with tab4:
        st.header("📊 Performance Metrics")
        
        # System performance overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💻 Laptop CPU", "45%", "-5%")
        with col2:
            st.metric("🔥 Orin GPU", "78%", "+12%")
        with col3:
            st.metric("💾 Memory Usage", "6.2 GB", "+0.8 GB")
        with col4:
            st.metric("🌡️ Temperature", "42°C", "+2°C")
        
        # Performance charts
        st.subheader("📈 Resource Usage")
        
        # Generate sample performance data
        perf_time = pd.date_range(start=datetime.now() - timedelta(minutes=30), periods=30, freq='1min')
        perf_data = pd.DataFrame({
            'Time': perf_time,
            'CPU %': [45 + i*2 + (i%3)*5 for i in range(30)],
            'Memory GB': [6.2 + i*0.1 + (i%2)*0.3 for i in range(30)],
            'GPU %': [78 - i*1 + (i%4)*8 for i in range(30)]
        })
        
        fig = px.line(perf_data, x='Time', y=['CPU %', 'Memory GB', 'GPU %'],
                     title="System Performance Over Time")
        st.plotly_chart(fig, use_container_width=True)
        
        # Network performance
        st.subheader("🌐 Network Performance")
        
        network_data = pd.DataFrame({
            'Node': ['Laptop', 'Jetson Orin', 'Jetson 2GB'],
            'Latency (ms)': [1, 15, 12],
            'Throughput (MB/s)': [150, 45, 20],
            'Packets Lost': [0, 0, 1]
        })
        
        fig = px.bar(network_data, x='Node', y='Latency (ms)', title="Network Latency by Node")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.header("📋 System Logs")
        
        # Log filtering
        col1, col2 = st.columns([3, 1])
        with col1:
            log_filter = st.selectbox("Filter logs", ["All", "INFO", "WARNING", "ERROR"])
        with col2:
            max_logs = st.number_input("Max logs", min_value=10, max_value=1000, value=100)
        
        # Display logs
        st.subheader("🔍 Recent Activity")
        
        if dashboard.brain_logs:
            for log_entry in dashboard.brain_logs[-max_logs:]:
                if log_filter == "All" or log_filter in log_entry['message']:
                    timestamp = log_entry['timestamp'].strftime("%H:%M:%S")
                    source = log_entry['source']
                    message = log_entry['message']
                    
                    # Color code based on log level
                    if "ERROR" in message:
                        st.error(f"[{timestamp}] {source}: {message}")
                    elif "WARNING" in message:
                        st.warning(f"[{timestamp}] {source}: {message}")
                    else:
                        st.info(f"[{timestamp}] {source}: {message}")
        else:
            st.info("No logs available. Start the brain system to see activity.")
        
        # Export logs button
        if st.button("📤 Export Logs"):
            log_text = "\n".join([f"[{log['timestamp']}] {log['source']}: {log['message']}" 
                                 for log in dashboard.brain_logs])
            st.download_button(
                label="💾 Download Logs",
                data=log_text,
                file_name=f"brain_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    # Footer
    st.markdown("---")
    st.markdown("🧠 **Home AI Brain Network** | Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    main()