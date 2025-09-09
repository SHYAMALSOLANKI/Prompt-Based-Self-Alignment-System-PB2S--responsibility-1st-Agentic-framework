from fastapi import FastAPI
from pydantic import BaseModel
import time, uuid

app = FastAPI(title="PB2S Minimal /chat Server", version="0.1.0")

class ChatIn(BaseModel):
    message: str

@app.post("/chat")
def chat(body: ChatIn):
    # Minimal, structure-complete reply (mock). Swap with your model later.
    draft = f"- Initial take on: {body.message}"
    reflect = (
        "- contradiction: none material; check evidence sources\n"
        "- unjustified assumption: clarify scope\n"
        "- missing evidence: cite at least one source type"
    )
    revise = "- adjusted explanation with scope + reference types"
    learned = "- concise takeaways"

    text = (
        "DRAFT\n" + draft + "\n\n" +
        "REFLECT\n" + reflect + "\n\n" +
        "REVISE\n" + revise + "\n\n" +
        "LEARNED\n" + learned
    )

    proof = {
        "decision": "APPROVE",
        "cycles": 1,
        "audit_ref": f"run-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"
    }
    return {"text": text, "pb2s_proof": proof}

# Run locally:
# uvicorn server.main:app --reload --port 8000
