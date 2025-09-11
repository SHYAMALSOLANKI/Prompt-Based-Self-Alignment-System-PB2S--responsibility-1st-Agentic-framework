"""
core-b: Jetson Core Service (PB2S Planner, Attention/Focus, CAE, Memory Hub)
Minimal FastAPI skeleton for PB2S multi-node deployment.
"""
from fastapi import FastAPI

app = FastAPI(title="core-b (Jetson Core)", version="0.1.0")

@app.get("/")
def root():
    return {"status": "core-b up", "role": "PB2S planner, attention, CAE, memory"}
