# JETSON RESCUE GUIDE - Get PB2S Running TODAY

## STEP 1: Check your current location
```bash
pwd
ls
```
You should be in: `/home/pb2s_brain/GitHub/PB2S_1/`

## STEP 2: Install Python packages directly (no requirements.txt needed)
```bash
pip install uvicorn fastapi aiohttp asyncio-mqtt websockets openai scikit-learn opencv-python matplotlib pydantic python-multipart
```

## STEP 3: Create a simple PB2S brain server
Save this as `simple_brain.py` in your PB2S_1 folder:

```python
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
```

## STEP 4: Run the brain server
```bash
python3 simple_brain.py
```

## STEP 5: Test from another terminal or your laptop
```bash
curl -X POST http://10.224.0.138:8000/chat -H "Content-Type: application/json" -d '{"message": "Hello PB2S brain!"}'
```

## STEP 6: Add LLM capability (optional - after basic works)
Install LLM packages:
```bash
pip install transformers torch
```

That's it! Your PB2S brain will be running on port 8000.