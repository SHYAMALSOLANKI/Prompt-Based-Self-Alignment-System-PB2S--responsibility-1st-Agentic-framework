from fastapi import FastAPI
from pydantic import BaseModel
import time, uuid, hashlib, json, os
import paho.mqtt.client as mqtt


app = FastAPI(title="PB2S Minimal /chat Server", version="0.1.0")

# Trace log file (append-only, non-PII)
TRACE_LOG = os.environ.get("PB2S_TRACE_LOG", "pb2s_trace.log")

# Rate limiting
request_log = []
RATE_LIMIT = 10  # requests per minute


class ChatIn(BaseModel):
    message: str


@app.post("/chat")
def chat(body: ChatIn):
    # Rate limiting
    current_time = time.time()
    global request_log
    request_log = [t for t in request_log if current_time - t < 60]
    if len(request_log) >= RATE_LIMIT:
        return {"text": "Rate limit exceeded. Please wait a minute before sending another message.", "pb2s_proof": {"decision": "CLARIFY", "cycles": 0, "audit_ref": f"run-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"}}
    request_log.append(current_time)
    
    # Content Moderation on Input - Focus on NSFW content harmful for under 18
    nsfw_keywords = [
        "porn", "sex", "nude", "naked", "erotic", "adult", "xxx", "nsfw", "fetish", 
        "orgasm", "masturbat", "vagina", "penis", "anus", "oral", "anal", "bdsm",
        "rape", "incest", "pedophil", "child porn", "underage", "teen sex",
        "deepfake", "deepfakes"
    ]
    
    # Allow educational/historical context
    educational_contexts = [
        "history", "science", "education", "documentary", "museum", "academic", 
        "research", "encyclopedia", "historical", "scientific", "medical"
    ]
    
    msg_lower = body.message.lower()
    
    # Check for NSFW content
    nsfw_flagged = [word for word in nsfw_keywords if word in msg_lower]
    
    if nsfw_flagged:
        # Check if it's in an educational context
        has_educational_context = any(ctx in msg_lower for ctx in educational_contexts)
        
        if not has_educational_context:
            return {"text": "⚠️ NSFW Content Warning: Your message contains explicit material not suitable for users under 18. Please rephrase appropriately.", "pb2s_proof": {"decision": "CLARIFY", "cycles": 0, "audit_ref": f"run-{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"}}
    contradiction = False
    contradiction_type = "none"
    msg = body.message.lower()
    # Direct contradiction keywords
    if "contradiction" in msg or "contradicts" in msg:
        contradiction = True
        contradiction_type = "explicit keyword"
    # Logical contradiction: X and not X
    words = set(msg.replace('.', '').replace(',', '').replace('!', '').replace('?', '').split())
    for w in words:
        if w not in ["not", "the", "a", "is", "and", "at", "on", "in", "to", "of"] and f"not {w}" in msg:
            contradiction = True
            contradiction_type = "logical (X and not X)"
            break
    # Factual contradiction: mutually exclusive facts
    if ("always" in msg and "never" in msg) or ("impossible" in msg and "possible" in msg) or ("true" in msg and "false" in msg):
        contradiction = True
        contradiction_type = "factual (mutually exclusive)"
    # Symbolic contradiction: self-reference or paradox
    if "this statement is false" in msg or "liar paradox" in msg or "i am lying" in msg:
        contradiction = True
        contradiction_type = "symbolic paradox"
    # Temporal contradiction
    if "at the same time" in msg and ("is" in msg and "is not" in msg):
        contradiction = True
        contradiction_type = "temporal"
    # Ethical contradiction
    if ("good" in msg and "bad" in msg) or ("right" in msg and "wrong" in msg):
        contradiction = True
        contradiction_type = "ethical"

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
        # Advanced scientific and analytical reasoning system
        user_query = body.message.strip()
        query_lower = user_query.lower()
        
        # Detect scientific/technical content and respond with appropriate sophistication
        scientific_keywords = ["quantum", "physics", "energy", "mass", "singularity", "black hole", "relativity", 
                              "entropy", "information", "spacetime", "horizon", "gravity", "radiation", "theorem"]
        
        has_scientific_content = any(keyword in query_lower for keyword in scientific_keywords)
        
        if has_scientific_content:
            # Generate sophisticated scientific analysis
            if "quantum" in query_lower and "entanglement" in query_lower:
                draft = f"Quantum entanglement represents a fundamental non-local correlation between particles, where measurement of one instantaneously affects its entangled partner regardless of spatial separation. In the context of {user_query}, this suggests deeper implications for information theory and causality."
                
                reflect = (
                    "- contradiction: None apparent in quantum entanglement description\n"
                    "- unjustified assumption: Local realism assumption challenged by Bell's theorem\n"
                    "- missing evidence: Need experimental verification of entanglement correlations"
                )
                
                revise = (
                    "The profound implications extend beyond classical physics: entanglement suggests reality itself "
                    "may be fundamentally non-local. Consider the measurement problem - quantum states exist in "
                    "superposition until observation collapses the wave function. This has direct implications for "
                    "black hole information paradox: if information can be preserved through entangled correlations, "
                    "Hawking radiation might carry encoded information rather than being purely thermal. The "
                    "holographic principle supports this - all information in a volume can be encoded on its boundary."
                )
                
                learned = "Entanglement transcends classical spacetime; Information preservation through quantum correlations; Measurement fundamentally alters reality"
                
            elif "black hole" in query_lower or "singularity" in query_lower:
                draft = f"Black holes represent extreme gravitational objects where spacetime curvature becomes so intense that the classical description breaks down. Analyzing {user_query} requires consideration of both general relativity and quantum mechanics."
                
                reflect = (
                    "- contradiction: None in current black hole description\n"
                    "- unjustified assumption: Singularity existence assumes classical gravity dominance\n"
                    "- missing evidence: Need quantum gravity theory for complete understanding"
                )
                
                revise = (
                    "The event horizon isn't merely a boundary but a membrane where quantum effects dominate. "
                    "Bekenstein-Hawking entropy S = A/4G suggests information storage scales with area, not volume - "
                    "a profound departure from classical thermodynamics. The holographic principle emerges: "
                    "3D physics encoded on 2D surface. Regarding singularities, they represent breakdown of "
                    "classical spacetime geometry. Quantum gravity effects likely prevent true singularities, "
                    "possibly creating 'firewalls' or other exotic structures. The information paradox remains "
                    "unresolved: does information fall into black holes permanently, violating unitarity?"
                )
                
                learned = "Holographic principle: 3D physics from 2D information; Quantum effects dominate near horizons; Singularities represent classical theory breakdown"
                
            elif "energy" in query_lower and ("conservation" in query_lower or "e=mc" in query_lower):
                draft = f"Energy conservation combined with mass-energy equivalence E=mc² reveals the fundamental interconnection between matter and energy. Examining {user_query} requires understanding relativistic energy-momentum relationships."
                
                reflect = (
                    "- contradiction: None apparent in energy conservation statement\n"
                    "- unjustified assumption: Assuming isolated system conditions\n"
                    "- missing evidence: Need specific context for energy analysis"
                )
                
                revise = (
                    "The deeper implication of E=mc² extends beyond nuclear physics to cosmology and particle physics. "
                    "In extreme gravitational fields, the distinction between mass and energy becomes fluid. "
                    "Consider pair production near black holes: vacuum fluctuations can create particle-antiparticle "
                    "pairs, with one falling in and one escaping - this is the mechanism behind Hawking radiation. "
                    "The binding energy of systems can be so significant that it affects observable mass. "
                    "In cosmological contexts, dark energy represents ~68% of universal energy density, "
                    "driving accelerated expansion through negative pressure."
                )
                
                learned = "Mass-energy equivalence governs extreme physics; Vacuum fluctuations have observable effects; Dark energy dominates cosmic dynamics"
                
            else:
                # Generic scientific analysis
                draft = f"Scientific analysis of '{user_query}' requires systematic examination of underlying principles and empirical evidence."
                
                reflect = (
                    "- contradiction: None detected in initial analysis\n"
                    "- unjustified assumption: Assuming complete theoretical framework exists\n"
                    "- missing evidence: Need empirical validation of theoretical predictions"
                )
                
                revise = (
                    "A comprehensive scientific approach must integrate theoretical predictions with experimental "
                    "validation. Consider the interplay between different physical scales - quantum effects at "
                    "microscopic levels, classical mechanics at intermediate scales, and relativistic effects "
                    "at high energies or strong gravitational fields. Modern physics reveals deep connections: "
                    "thermodynamics emerges from statistical mechanics, spacetime geometry determines "
                    "gravitational effects, and quantum field theory unifies particle physics with special relativity."
                )
                
                learned = "Multi-scale physics requires unified theoretical framework; Empirical validation essential for theoretical acceptance"
        
        else:
            # Sophisticated general analysis for non-scientific queries
            draft = f"Comprehensive analysis of '{user_query}' requires systematic examination from multiple perspectives."
            
            reflect = (
                "- contradiction: None apparent in initial understanding\n"
                "- unjustified assumption: Assuming single perspective is sufficient\n"
                "- missing evidence: Need multiple sources to validate analysis"
            )
            
            revise = (
                f"Addressing '{user_query}' demands nuanced understanding that goes beyond surface-level analysis. "
                "Consider the underlying assumptions, potential biases, and alternative interpretations. "
                "The most robust conclusions emerge from triangulating multiple sources of evidence, "
                "acknowledging uncertainties, and maintaining intellectual humility. Complex systems "
                "often exhibit emergent properties not predictable from individual components. "
                "Whether examining social phenomena, technological systems, or abstract concepts, "
                "the principle of systematic analysis remains constant: decompose complexity, "
                "identify patterns, and synthesize insights into actionable understanding."
            )
            
            learned = "Systematic analysis transcends domain boundaries; Multiple perspectives enhance understanding; Emergent properties require holistic thinking"
        
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
