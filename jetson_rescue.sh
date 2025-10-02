#!/bin/bash

# JETSON RESCUE SCRIPT - One-click setup for PB2S
# Run this on your Jetson to get PB2S working

echo "=== JETSON RESCUE SCRIPT - PB2S Setup ==="
echo "This will get your Jetson running with PB2S today!"
echo ""

# Step 1: Go to the correct directory
echo "Step 1: Going to PB2S_1 folder..."
cd /home/pb2s_brain/GitHub/PB2S_1 || {
    echo "ERROR: Cannot find PB2S_1 folder. Checking alternatives..."
    if [ -d "/home/shyamal/PB2S_1" ]; then
        cd /home/shyamal/PB2S_1
        echo "Found PB2S_1 in /home/shyamal/"
    elif [ -d "/home/shyamal/Prompt-Based-Self-Alignment-System-PB2S--responsibility-1st-Agentic-framework" ]; then
        cd /home/shyamal/Prompt-Based-Self-Alignment-System-PB2S--responsibility-1st-Agentic-framework
        echo "Found long folder name"
    else
        echo "Please tell me where your PB2S files are located!"
        exit 1
    fi
}

# Step 2: Check if we have the right files
echo "Step 2: Checking for required files..."
if [ ! -f "requirements.txt" ]; then
    echo "WARNING: requirements.txt not found. Will install packages manually."
    MANUAL_INSTALL=true
else
    echo "Found requirements.txt"
    MANUAL_INSTALL=false
fi

# Step 3: Install packages
echo "Step 3: Installing Python packages..."
if [ "$MANUAL_INSTALL" = true ]; then
    echo "Installing packages manually..."
    pip3 install fastapi uvicorn aiohttp asyncio-mqtt websockets openai scikit-learn opencv-python matplotlib numpy pandas
else
    echo "Installing from requirements.txt..."
    pip3 install -r requirements.txt
fi

# Step 4: Check if server directory exists
echo "Step 4: Checking server files..."
if [ ! -d "server" ]; then
    echo "ERROR: server folder not found!"
    echo "Current directory contents:"
    ls -la
    exit 1
fi

# Step 5: Create a simple startup script
echo "Step 5: Creating startup script..."
cat > start_pb2s.py << 'EOF'
#!/usr/bin/env python3
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.getcwd())

try:
    import uvicorn
    print("Starting PB2S server...")
    print("Server will run on: http://0.0.0.0:8000")
    print("Access from laptop: http://10.224.0.138:8000")
    print("Press Ctrl+C to stop")
    uvicorn.run('server.main:app', host='0.0.0.0', port=8000, reload=False)
except ImportError as e:
    print(f"Error: {e}")
    print("Please install missing packages:")
    print("pip3 install uvicorn fastapi")
except Exception as e:
    print(f"Server error: {e}")
    print("Check if port 8000 is available")
EOF

chmod +x start_pb2s.py

# Step 6: Test basic functionality
echo "Step 6: Testing Python installation..."
python3 -c "print('Python is working!')"

echo ""
echo "=== RESCUE COMPLETE ==="
echo "To start PB2S server, run:"
echo "  python3 start_pb2s.py"
echo ""
echo "To test from laptop, run:"
echo "  curl -X POST http://10.224.0.138:8000/chat -H 'Content-Type: application/json' -d '{\"message\": \"Hello PB2S!\"}'"
echo ""
echo "Current directory: $(pwd)"
echo "Files available:"
ls -la

echo ""
echo "If you see any errors above, copy the error message and ask for help!"
