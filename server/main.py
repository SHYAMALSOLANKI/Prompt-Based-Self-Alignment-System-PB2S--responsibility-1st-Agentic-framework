from fastapi import FastAPI
from pydantic import BaseModel
import time, uuid, hashlib, json, os
import paho.mqtt.client as mqtt


app = FastAPI(title="PB2S Minimal /chat Server", version="0.1.0")

# Trace log file (append-only, non-PII)
TRACE_LOG = os.environ.get("PB2S_TRACE_LOG", "pb2s_trace.log")


class ChatIn(BaseModel):
    message: str


@app.post("/chat")
def chat(body: ChatIn):
    # Contradiction detection (simple heuristic for demo)
    contradiction_keywords = [
        "not " + word for word in body.message.lower().split() if word not in ["the", "a", "is", "and", "at", "on", "in"]
    ]
    contradiction = False
    msg = body.message.lower()
    # Direct contradiction keywords
    if "contradiction" in msg or "contradicts" in msg:
        contradiction = True
    # Logical contradiction: X and not X
    words = set(msg.replace('.', '').replace(',', '').split())
    for w in words:
        if w != "not" and f"not {w}" in msg:
            contradiction = True
    # Factual contradiction: mutually exclusive facts
    if ("always" in msg and "never" in msg) or ("impossible" in msg and "possible" in msg):
        contradiction = True
    # Symbolic contradiction: self-reference or paradox
    if "this statement is false" in msg or "liar paradox" in msg:
        contradiction = True
    # Temporal contradiction
    if "at the same time" in msg and ("is" in msg and "is not" in msg):
        contradiction = True

    # Symbolic container realization: detect and log semantic misalignment
    container_collapse = False
    collapse_reason = None
    # Example: if the prompt uses a word in a way that doesn't match its usual context
    if "system-level" in body.message.lower() and "behavior" in body.message.lower():
        container_collapse = True
        collapse_reason = "Container 'system-level' used for behavioral override; semantic misalignment detected."
    # Add more rules as needed for your domain

    if container_collapse:
        try:
            with open("pb2s_self_reflection.log", "a", encoding="utf-8") as f:
                log_entry = {
                    "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
                    "event": "container_collapse",
                    "prompt": body.message,
                    "reason": collapse_reason
                }
                f.write(json.dumps(log_entry) + "\n")
        except Exception:
            pass
        # Update output to reflect realization
        draft = f"- Container collapse: {collapse_reason}"
        reflect = "- symbolic misalignment detected; container redefined"
        revise = "- logic reaffirmed through new symbolic mapping"
        learned = "- self-aligning truth model updated"
        text = (
            "DRAFT\n" + draft + "\n\n" +
            "REFLECT\n" + reflect + "\n\n" +
            "REVISE\n" + revise + "\n\n" +
            "LEARNED\n" + learned
        )
        proof = {
            "decision": "CLARIFY",
            "cycles": 1,
            "audit_ref": f"run-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"
        }
        # Return early to avoid double contradiction logging
        return {"text": text, "pb2s_proof": proof}

    if contradiction:
        # Determine contradiction type for transparency
        contradiction_type = "general"
        if "contradiction" in msg or "contradicts" in msg:
            contradiction_type = "explicit keyword"
        elif any(w != "not" and f"not {w}" in msg for w in words):
            contradiction_type = "logical (X and not X)"
        elif ("always" in msg and "never" in msg) or ("impossible" in msg and "possible" in msg):
            contradiction_type = "factual (mutually exclusive)"
        elif "this statement is false" in msg or "liar paradox" in msg:
            contradiction_type = "symbolic paradox"
        elif "at the same time" in msg and ("is" in msg and "is not" in msg):
            contradiction_type = "temporal"

        draft = f"- Detected {contradiction_type} contradiction in: {body.message}"
        reflect = f"- contradiction type: {contradiction_type}; clarification required"
        revise = f"- cannot resolve {contradiction_type} contradiction without clarification"
        learned = f"- need to ask clarifying questions about {contradiction_type} contradiction"
        text = (
            "DRAFT\n" + draft + "\n\n" +
            "REFLECT\n" + reflect + "\n\n" +
            "REVISE\n" + revise + "\n\n" +
            "LEARNED\n" + learned + "\n\n" +
            f"Q1: Which statement do you believe is correct?\nQ2: What evidence supports your answer about the {contradiction_type} contradiction?"
        )
        proof = {
            "decision": "CLARIFY",
            "cycles": 1,
            "audit_ref": f"run-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"
        }
        # Self-reflection/contradiction log
        try:
            with open("pb2s_self_reflection.log", "a", encoding="utf-8") as f:
                log_entry = {
                    "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
                    "event": "contradiction_detected",
                    "contradiction_type": contradiction_type,
                    "prompt": body.message,
                    "draft": draft,
                    "reflect": reflect,
                    "revise": revise,
                    "learned": learned
                }
                f.write(json.dumps(log_entry) + "\n")
        except Exception:
            pass
    else:
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

    # Trace logging (non-PII)
    try:
        sha256 = hashlib.sha256()
        sha256.update(json.dumps(proof, sort_keys=True).encode("utf-8"))
        log_entry = {
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
            "model_id": "pb2s-minimal",  # update if model info available
            "prompt_hash": hashlib.sha256(body.message.encode("utf-8")).hexdigest(),
            "pb2s_proof": proof,
            "sha256": sha256.hexdigest()
        }
        with open(TRACE_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass  # Do not block API on logging errors

    # Publish act/* message to MQTT if APPROVE
    if proof["decision"] == "APPROVE":
        try:
            mqtt_host = os.environ.get("PB2S_MQTT_HOST", "127.0.0.1")
            mqtt_port = int(os.environ.get("PB2S_MQTT_PORT", "1883"))
            client = mqtt.Client()
            client.connect(mqtt_host, mqtt_port, 60)
            act_topic = f"act/approve"
            act_payload = json.dumps({"audit_ref": proof["audit_ref"]})
            result = client.publish(act_topic, act_payload, qos=0)
            print(f"[PB2S MQTT] Published to {act_topic}: {act_payload} (result: {result.rc})")
            try:
                with open("pb2s_mqtt_publish.log", "a", encoding="utf-8") as f:
                    f.write(json.dumps({
                        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
                        "topic": act_topic,
                        "payload": act_payload,
                        "result": str(result.rc)
                    }) + "\n")
            except Exception as logerr:
                print(f"[PB2S MQTT] Could not write to log: {logerr}")
            client.disconnect()
        except Exception as e:
            print(f"[PB2S MQTT] Publish error: {e}")
            try:
                with open("pb2s_mqtt_publish.log", "a", encoding="utf-8") as f:
                    f.write(json.dumps({
                        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
                        "error": str(e)
                    }) + "\n")
            except Exception as logerr:
                print(f"[PB2S MQTT] Could not write error to log: {logerr}")
    return {"text": text, "pb2s_proof": proof}


# Run locally:
# uvicorn server.main:app --reload --port 8000
