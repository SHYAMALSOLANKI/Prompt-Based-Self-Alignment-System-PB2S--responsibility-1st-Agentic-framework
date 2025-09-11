"""
pi-a: Audio/Intent Service (ASR, TTS)
Minimal FastAPI skeleton for PB2S multi-node deployment.
"""
from fastapi import FastAPI

app = FastAPI(title="pi-a (Audio/Intent)", version="0.1.0")

@app.get("/")
def root():
    return {"status": "pi-a up", "role": "audio intent, TTS"}
