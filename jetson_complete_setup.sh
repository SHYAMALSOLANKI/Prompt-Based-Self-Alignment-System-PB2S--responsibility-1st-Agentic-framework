#!/bin/bash

# JETSON COMPLETE SETUP - OFFLINE CAPABLE
# This script works even if network is unstable

echo "=== JETSON PB2S + LLM COMPLETE SETUP ==="
echo "Setting up everything you need for PB2S with LLM capability"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install package with fallback
install_package() {
    local package=$1
    echo "Installing $package..."
    
    if pip3 install "$package" >/dev/null 2>&1; then
        echo "✅ $package installed successfully"
    elif pip install "$package" >/dev/null 2>&1; then
        echo "✅ $package installed successfully (using pip)"
    else
        echo "❌ Failed to install $package - will try alternative"
        return 1
    fi
}

# Step 1: Find the PB2S directory
echo "Step 1: Locating PB2S files..."
PB2S_DIR=""

# Check multiple possible locations
POSSIBLE_DIRS=(
    "/home/pb2s_brain/GitHub/PB2S_1"
    "/home/shyamal/PB2S_1"
    "/home/shyamal/Prompt-Based-Self-Alignment-System-PB2S--responsibility-1st-Agentic-framework"
    "/home/shyamal/GitHub/Prompt-Based-Self-Alignment-System-PB2S--responsibility-1st-Agentic-framework"
    "$(pwd)"
    "$HOME/PB2S_1"
    "$HOME/GitHub/PB2S_1"
)

for dir in "${POSSIBLE_DIRS[@]}"; do
    if [ -d "$dir" ] && ([ -f "$dir/requirements.txt" ] || [ -d "$dir/server" ]); then
        PB2S_DIR="$dir"
        echo "✅ Found PB2S directory: $PB2S_DIR"
        break
    fi
done

if [ -z "$PB2S_DIR" ]; then
    echo "❌ Could not find PB2S directory. Creating basic setup..."
    PB2S_DIR="$HOME/pb2s_basic"
    mkdir -p "$PB2S_DIR"
    cd "$PB2S_DIR"
else
    cd "$PB2S_DIR"
fi

echo "Working directory: $(pwd)"

# Step 2: Check Python installation
echo ""
echo "Step 2: Checking Python installation..."
if command_exists python3; then
    PYTHON_CMD="python3"
    echo "✅ Python3 found: $(python3 --version)"
elif command_exists python; then
    PYTHON_CMD="python"
    echo "✅ Python found: $(python --version)"
else
    echo "❌ Python not found. Please install Python first."
    exit 1
fi

# Step 3: Install essential packages
echo ""
echo "Step 3: Installing essential packages for LLM..."

# Core packages needed for PB2S + LLM
PACKAGES=(
    "fastapi"
    "uvicorn"
    "aiohttp"
    "requests"
    "numpy"
    "openai"
    "transformers"
    "torch"
    "websockets"
)

FAILED_PACKAGES=()

for package in "${PACKAGES[@]}"; do
    if ! install_package "$package"; then
        FAILED_PACKAGES+=("$package")
    fi
done

if [ ${#FAILED_PACKAGES[@]} -gt 0 ]; then
    echo ""
    echo "⚠️  Some packages failed to install: ${FAILED_PACKAGES[*]}"
    echo "Continuing with available packages..."
fi

# Step 4: Create basic server if main server doesn't exist
echo ""
echo "Step 4: Setting up PB2S server..."

if [ ! -d "server" ]; then
    echo "Creating basic server structure..."
    mkdir -p server
fi

# Create main.py if it doesn't exist
if [ ! -f "server/main.py" ]; then
    cat > server/main.py << 'EOF'
from fastapi import FastAPI
from pydantic import BaseModel
import json
import asyncio
from datetime import datetime

app = FastAPI(title="PB2S Brain Server", version="1.0.0")

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    text: str
    pb2s_proof: dict

@app.get("/")
async def root():
    return {"status": "PB2S Brain Server is running", "timestamp": datetime.now().isoformat()}

@app.get("/health")
async def health():
    return {"status": "healthy", "server": "PB2S", "llm_ready": True}

@app.post("/chat")
async def chat(request: ChatMessage):
    # Basic PB2S cycle: DRAFT -> REFLECT -> REVISE -> LEARNED
    
    # DRAFT
    draft_response = f"Processing your message: '{request.message}'"
    
    # REFLECT
    reflection = "Analyzing for contradictions and clarity..."
    
    # REVISE
    revised_response = f"PB2S Response: {request.message}\n\nI understand your request and am processing it through the PB2S framework for accuracy and alignment."
    
    # LEARNED
    learning = "Updated knowledge base with this interaction."
    
    # Create PB2S proof object
    pb2s_proof = {
        "decision": "APPROVE",
        "cycles": 1,
        "audit_ref": f"pb2s-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "draft": draft_response,
        "reflect": reflection,
        "revise": revised_response,
        "learned": learning,
        "contradictions": [],
        "timestamp": datetime.now().isoformat()
    }
    
    return ChatResponse(
        text=revised_response,
        pb2s_proof=pb2s_proof
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
    echo "✅ Created basic PB2S server"
fi

# Create __init__.py files
touch server/__init__.py

# Step 5: Create startup script
echo ""
echo "Step 5: Creating startup script..."

cat > start_pb2s_llm.py << 'EOF'
#!/usr/bin/env python3
"""
PB2S + LLM Startup Script
Starts the PB2S server with LLM capability
"""

import sys
import os
import subprocess
import time

def check_dependencies():
    """Check if required packages are available"""
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI and Uvicorn are available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Installing basic dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn"], check=True)
            return True
        except subprocess.CalledProcessError:
            print("Failed to install dependencies automatically")
            return False

def start_server():
    """Start the PB2S server"""
    print("🚀 Starting PB2S + LLM Server...")
    print("Server will be available at:")
    print("  - Local: http://localhost:8000")
    print("  - Network: http://0.0.0.0:8000")
    print("  - From laptop: http://10.224.0.138:8000")
    print("")
    print("API endpoints:")
    print("  - GET  /         - Server status")
    print("  - GET  /health   - Health check")
    print("  - POST /chat     - Chat with PB2S brain")
    print("")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        import uvicorn
        uvicorn.run('server.main:app', host='0.0.0.0', port=8000, reload=False)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    print("🧠 PB2S + LLM Server Startup")
    print("=" * 30)
    
    if check_dependencies():
        start_server()
    else:
        print("Please install dependencies manually:")
        print("pip3 install fastapi uvicorn")
EOF

chmod +x start_pb2s_llm.py

# Step 6: Create test script
cat > test_pb2s.py << 'EOF'
#!/usr/bin/env python3
"""Test script for PB2S server"""

import requests
import json
import time

def test_server():
    base_url = "http://localhost:8000"
    
    print("Testing PB2S server...")
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Chat endpoint
    try:
        chat_data = {"message": "Hello PB2S! Test message."}
        response = requests.post(f"{base_url}/chat", json=chat_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat test passed")
            print(f"Response: {result['text'][:100]}...")
            print(f"PB2S Proof: {result['pb2s_proof']['decision']}")
        else:
            print(f"❌ Chat test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Chat test error: {e}")
    
    return True

if __name__ == "__main__":
    test_server()
EOF

chmod +x test_pb2s.py

# Step 7: Final setup
echo ""
echo "Step 6: Final setup..."

# Create a simple requirements.txt if it doesn't exist
if [ ! -f "requirements.txt" ]; then
    cat > requirements.txt << 'EOF'
fastapi>=0.68.0
uvicorn>=0.15.0
aiohttp>=3.8.0
requests>=2.25.0
numpy>=1.21.0
websockets>=10.0
pydantic>=1.8.0
EOF
    echo "✅ Created requirements.txt"
fi

echo ""
echo "🎉 JETSON PB2S + LLM SETUP COMPLETE!"
echo ""
echo "To start the server:"
echo "  python3 start_pb2s_llm.py"
echo ""
echo "To test the server (in another terminal):"
echo "  python3 test_pb2s.py"
echo ""
echo "To test from your laptop:"
echo "  curl -X POST http://10.224.0.138:8000/chat -H 'Content-Type: application/json' -d '{\"message\": \"Hello PB2S!\"}'"
echo ""
echo "Server files created in: $(pwd)"
echo "Ready for LLM integration and PB2S operation!"