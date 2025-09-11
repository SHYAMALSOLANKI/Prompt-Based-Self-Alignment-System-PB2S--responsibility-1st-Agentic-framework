from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.testclient import TestClient
import hashlib, time, uuid, json

# --- PB2S Planner Mock (Proof v2) ---
app = FastAPI(title="PB2S Planner Mock (Proof v2)")

class ChatRequest(BaseModel):
    context: dict | None = None
    facts: list[str] = []
    policy: dict = {}

SEED = 123456
def sha256_bytes(b: bytes) -> str: return "sha256:" + hashlib.sha256(b).hexdigest()
MODEL_SHA, POLICY_SHA = sha256_bytes(b"planner-model-mock"), sha256_bytes(b"pb2s-policy-mock")

@app.post("/chat")
def chat(_req: ChatRequest):
    t0 = time.time()
    text = (
        "DRAFT\n- initial take based on context\n\n"
        "REFLECT\n- contradiction: none\n- unstated assumption: clarify scope\n- missing evidence: cite at least one source type\n\n"
        "REVISE\n- revised answer with scope + reference types\n\n"
        "LEARNED\n- concise takeaway"
    )
    proof = {
        "decision":"APPROVE","cycles":1,
        "audit_ref":f"run-{int(time.time())}-{uuid.uuid4().hex[:8]}",
        "model_sha":MODEL_SHA,"policy_sha":POLICY_SHA,
        "attention_state":"FAIR","cr_event":{"old":"idle","new":"answer_prepared"},
        "bus_msg_id":str(uuid.uuid4()),
        "sampler":{"seed":SEED,"temperature":0.2,"top_p":0.9,"top_k":50},
        "timings":{"draft_ms":8,"reflect_ms":6,"revise_ms":7,"total_ms":int((time.time()-t0)*1000)}
    }
    return {"text":text, "pb2s_proof":proof}

# --- Call it locally (no HTTP) ---
client = TestClient(app)
resp = client.post("/chat", json={"context":{},"facts":[],"policy":{"maxCycles":2,"temp":0.2}})
print(json.dumps(resp.json(), indent=2))
