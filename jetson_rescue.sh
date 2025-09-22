#!/bin/bash
# JETSON RESCUE SCRIPT - One command to get PB2S running

echo "=== JETSON PB2S RESCUE SCRIPT ==="
echo "This will get your PB2S brain running in 5 minutes!"

# Install required packages
echo "Step 1: Installing Python packages..."
pip install uvicorn fastapi aiohttp asyncio-mqtt websockets openai scikit-learn opencv-python matplotlib pydantic python-multipart

# Create simple brain server
echo "Step 2: Creating PB2S brain server..."
cat > simple_brain.py << 'EOF'
from fastapi import FastAPI
import uvicorn
import json
from datetime import datetime

app = FastAPI(title="PB2S Brain Server")

@app.get("/")
def read_root():
    return {"message": "PB2S Brain is running!", "status": "active", "time": datetime.now()}

@app.post("/chat")
def chat_with_brain(message: dict):
    user_input = message.get("message", "")
    
    # Simple PB2S cycle simulation
    draft = f"DRAFT: Processing '{user_input}'"
    reflect = f"REFLECT: Checking for contradictions in '{user_input}'"
    revise = f"REVISE: Refined response for '{user_input}'"
    learned = f"LEARNED: Stored knowledge about '{user_input}'"
    
    response = {
        "text": f"{draft}\n{reflect}\n{revise}\n{learned}",
        "pb2s_proof": {
            "decision": "APPROVE",
            "cycles": 1,
            "audit_ref": f"run-{datetime.now().timestamp()}"
        }
    }
    
    return response

@app.get("/health")
def health_check():
    return {"status": "healthy", "brain": "active"}

if __name__ == "__main__":
    print("Starting PB2S Brain Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

echo "Step 3: Making script executable..."
chmod +x simple_brain.py

echo "=== RESCUE COMPLETE ==="
echo "To start your PB2S brain, run:"
echo "python3 simple_brain.py"
echo ""
echo "To test it, open another terminal and run:"
echo "curl -X POST http://localhost:8000/chat -H 'Content-Type: application/json' -d '{\"message\": \"Hello PB2S!\"}'"