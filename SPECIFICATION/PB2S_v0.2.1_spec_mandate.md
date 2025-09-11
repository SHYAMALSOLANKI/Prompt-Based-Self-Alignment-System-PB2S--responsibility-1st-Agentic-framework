# PB2S v0.2.1.1 — Normative Completion (Source‑of‑Truth Embedded)

> **Status:** Normative completion of PB2S v0.2.1. This version closes all identified gaps (determinism, proof fields, timebase, heartbeat semantics, bus security, backpressure, retention) and embeds **Source‑of‑Truth (SOT)** anchors for CI. It does **not** alter the four‑step runtime (DRAFT→REFLECT→REVISE→LEARNED); it strengthens what MUST be proven around it.

---

## SOT — Source‑of‑Truth Anchors (for CI to verify)
- **SOT_SPEC_ID:** pb2s_v0.2.1.1  
- **SOT_COMMIT:** <filled‑by‑CI>  
- **SOT_SHA256:** <filled‑by‑CI over §§2–8 only>  
- **SOT_PROOF_SCHEMA:** /schemas/pb2s_proof.v2.schema.json  
- **SOT_TESTSET:** core + AT‑1..AT‑7  
- **SOT_GENERATED_AT:** <UTC‑ISO8601>

> CI SHALL compute the SHA‑256 digest of §§2–8 (normalized whitespace/CRLF) and fail if it does not match **SOT_SHA256**.

---

## 1) Scope & Invariants (unchanged runtime)
PB2S runtime remains: **DRAFT → REFLECT → REVISE → LEARNED**, with **maxCycles = 2**. If contradictions persist after REVISE, the decision SHALL be **CLARIFY** with **exactly two** questions targeting the unresolved gap. A **pb2s_proof** SHALL be attached to every planner reply.

---

## 2) Determinism Profile (per module) — NEW (MUST)
Each module participating in PB2S SHALL export a **Determinism Profile** JSON alongside binaries/config:
```json
{
  "module": "planner-core",
  "model_id": "<name>@<vers>",
  "model_sha": "sha256:…",
  "policy_sha": "sha256:…",           
  "seed": 123456,                       
  "temperature": 0.2,                   
  "top_p": 0.9, "top_k": 50,          
  "quant": "fp16" ,                    
  "nondeterminism": ["stt_timestamps"],
  "notes": "provider-specific caveats"
}
```
**MUSTs**
- Planner (the only text‑emitting node) SHALL use **temperature ≤ 0.2** and a fixed **seed** when supported.  
- Non‑planner nodes MUST NOT alter planner sampling params.
- CI SHALL re‑run a fixed prompt set 10× and assert identical **pb2s_proof** fields (except timestamps/latency) — see **AT‑3**.

---

## 3) Proof Object v2 — NEW (MUST)
All planner replies SHALL include **pb2s_proof v2**:
```json
{
  "decision": "APPROVE|DENY|CLARIFY",
  "cycles": 0,
  "audit_ref": "run-…",
  "model_sha": "sha256:…",
  "policy_sha": "sha256:…",
  "attention_state": "FAIR|TOTAL",
  "cr_event": {"old":"…","new":"…"},
  "bus_msg_id": "uuid",
  "sampler": {"seed":123456, "temperature":0.2, "top_p":0.9, "top_k":50},
  "timings": {"draft_ms":…, "reflect_ms":…, "revise_ms":…, "total_ms":…}
}
```
**MUSTs**: schema validation SHALL pass; `audit_ref` SHALL be propagated to all `act/*` topics derived from this decision (see **AT‑5**).

---

## 4) Time Base & Ordering — NEW (MUST)
- All nodes SHALL maintain **UTC wall clock** (NTP/Chrony) and a **monotonic** clock.  
- Logs and payloads SHALL carry `ts_utc` and MAY carry `ts_mono`.  
- CI SHALL reject proofs where `ts_utc` regresses or drifts > ±2 s from runner time.  
- Ordering within a run SHALL be by `ts_mono`.

---

## 5) Heartbeat & Halt Semantics — NEW (MUST)
- Attention Orchestrator heartbeat period: **20 ms**.  
- **Halt condition:** **two consecutive misses** (≥ 40 ms) SHALL force **actuator hold** at the MCU.  
- Heartbeat topics: `hb/<node>` QoS1.  
- **AT‑2** SHALL simulate missed heartbeats and assert hold behavior within 40 ms.

---

## 6) Bus Security & Keying — NEW (MUST)
- Broker links across subnets SHALL use **TLS** with per‑node credentials; topic‑level **ACLs** SHALL restrict `exec/*` to the planner.  
- **Maintenance tokens** SHALL be signed (ed25519). Actions performed under a token SHALL log the `key_id` and SHALL NOT bypass PB2S audit.  
- Secrets SHALL NOT appear in topics or logs.

---

## 7) Backpressure, QoS & Scheduling — NEW (MUST)
- **Allow‑list bridge**: ONLY `sym/*`, `sal/*`, `irq/*`, `planner/*`, `exec/*`, `hb/*`, `learn/*` MAY cross to the Big Brain.  
- **QoS**: `hb/*`=1, `planner/*`=1, `exec/*`=1, `sym/*`=0 or 1 (pref. 0), `irq/*`=1.  
- **Scheduling**: In **FAIR**, consumers SHALL implement **weighted round‑robin**; in **TOTAL**, non‑focused topics receive ε keep‑alive (≥ 1 msg/s).  
- Producers SHALL cap inflight publishes (e.g., 3) and **drop newest** on overflow.  
- CI **AT‑1** SHALL verify symbols‑only ingress; **AT‑6** SHALL verify ε keep‑alive under TOTAL.

---

## 8) Data Protection & Retention — NEW (MUST)
- **Retention**: hot logs ≥ 7 d; cold logs ≥ 60 d; both content‑hashed.  
- **PII**: face/audio hashes MAY be stored; raw assets MUST require consent flag; default is redact.  
- **Erasure**: signed request (ed25519) → tombstone index; purge within 30 d; audit entry emitted.  
- CI **AT‑7** SHALL assert the presence of retention config and that logs are content‑hashed.

---

## 9) Acceptance Tests (binding to spec)
- **AT‑1 Symbols‑Only Ingress**: publish `raw/*` at edge; expect no delivery to Core Bus; publish `sym/*`; expect delivery.  
- **AT‑2 Dead‑man Stop**: suppress `hb/*` ≥ 40 ms; verify actuator hold within 40 ms.  
- **AT‑3 Determinism**: 10× identical prompts at planner → identical `pb2s_proof` (excluding latency fields).  
- **AT‑4 CLARIFY Path**: unresolved contradiction → `decision=CLARIFY` + exactly **two** questions.  
- **AT‑5 Proof→Action Integrity**: every `act/*` carries planner `audit_ref` of last APPROVE.  
- **AT‑6 ε Keep‑Alive**: set TOTAL on vision; verify non‑vision topics still emit ≥1 msg/s.  
- **AT‑7 Retention & Hashing**: verify log store policy exists; sample artifacts have SHA‑256 fields.

---

## 10) SLOs (for evidence)
- **Intent latency** (Small→Big→reply): p95 ≤ 300 ms (FAIR), ≤ 120 ms (TOTAL).  
- **Vision symbol latency** (edge→attention event): p95 ≤ 120 ms.  
- **Safety**: 0 violations with `approve=false`; e‑stop ≤ 5 ms; dead‑man ≤ 40 ms.  
- **Uptime**: 24 h soak; no missed heartbeats.

---

## Appendix A — Proof v2 JSON‑Schema (path: /schemas/pb2s_proof.v2.schema.json)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "pb2s_proof.v2.schema.json",
  "type": "object",
  "required": ["decision","cycles","audit_ref","model_sha","policy_sha","sampler","timings"],
  "properties": {
    "decision": {"enum":["APPROVE","DENY","CLARIFY"]},
    "cycles": {"type":"integer","minimum":0,"maximum":2},
    "audit_ref": {"type":"string","minLength":8},
    "model_sha": {"type":"string"},
    "policy_sha": {"type":"string"},
    "attention_state": {"enum":["FAIR","TOTAL"]},
    "cr_event": {"type":"object"},
    "bus_msg_id": {"type":"string"},
    "sampler": {
      "type":"object",
      "required":["seed","temperature","top_p","top_k"],
      "properties":{
        "seed":{"type":"integer"},
        "temperature":{"type":"number","maximum":0.2},
        "top_p":{"type":"number","minimum":0,"maximum":1},
        "top_k":{"type":"integer","minimum":0}
      }
    },
    "timings": {
      "type":"object",
      "required":["draft_ms","reflect_ms","revise_ms","total_ms"],
      "properties":{
        "draft_ms":{"type":"number"},
        "reflect_ms":{"type":"number"},
        "revise_ms":{"type":"number"},
        "total_ms":{"type":"number"}
      }
    }
  }
}
```

## Appendix B — CI Binding (sot_verify invocation)
The CI SHALL run:
```
python scripts/sot_verify.py --spec "PB2S v0.2.1.1 — Normative Completion (Source‑of‑Truth Embedded)" \
  --sections 2..8 --schema schemas/pb2s_proof.v2.schema.json
```
…then run `conformance.py` and **AT‑1..AT‑7**.

