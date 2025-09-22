#!/bin/bash
# pb2s_quick_start.sh: One-click PB2S brain server start for Jetson

cd ~/Prompt-Based-Self-Alignment-System-PB2S--responsibility-1st-Agentic-framework
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -c "import uvicorn; uvicorn.run('server.main:app', host='0.0.0.0', port=8000)"
