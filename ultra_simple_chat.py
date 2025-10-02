#!/usr/bin/env python3
"""
Ultra-Simple PB2S Brain (Deterministic Demo)
Purpose: Provide a tiny, deterministic /chat endpoint that emits
		 DRAFT → REFLECT → REVISE → LEARNED plus a spec-aligned pb2s_proof v2.

Use cases:
- Local debugging of PB2S structure and proof without full stack
- Determinism testing (AT-3) and latency measurement

Run:
  python -m pip install fastapi uvicorn pydantic
  python -m uvicorn ultra_simple_chat:app --host 0.0.0.0 --port 8000
"""

import time
import uuid
import hashlib
from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="PB2S Ultra-Simple Brain", version="0.2.1-demo")


class ChatIn(BaseModel):
	message: str
	max_cycles: Optional[int] = 1
	time_budget_ms: Optional[int] = 300
	attention_state: Optional[str] = "FAIR"  # FAIR | TOTAL


def _sha256_hex(text: str) -> str:
	return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _now_run_id() -> str:
	return f"run-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"


def _reflect_points(draft: str, original: str):
	pts = []
	lower = (draft + "\n" + original).lower()
	# Ensure at least one of: contradiction, assumption, missing evidence
	if ("contradiction" in lower) or ("not " in lower and " is " in lower):
		pts.append("Flags a potential contradiction in the premise or wording")
	if "assume" in lower or "obvious" in lower or "clearly" in lower:
		pts.append("Identifies an implicit assumption requiring validation")
	if len(draft.split()) < 20 or any(k in lower for k in ["proof", "evidence", "source"]):
		pts.append("Notes missing evidence or insufficient context for certainty")

	if not pts:
		pts = [
			"Surfaces at least one assumption to verify",
			"Requests evidence for key claims",
			"Checks for hidden contradictions in terms"
		]
	return pts[:3]


@app.get("/status")
def status():
	return {"ok": True, "service": "pb2s-ultra-simple", "version": app.version}


@app.get("/chat")
def chat_get_hint():
	# Some existing tests probe GET /chat; return a friendly hint instead of 405.
	return {"ok": True, "hint": "Use POST /chat with { message }"}


@app.post("/chat")
def chat(body: ChatIn):
	t0 = time.perf_counter()
	# Deterministic sampler (spec-aligned defaults for planner-like behavior)
	sampler = {"seed": 42, "temperature": 0.2, "top_p": 0.9, "top_k": 50}

	# Minimal deterministic PB2S cycle (bounded by max_cycles/time_budget_ms)
	# DRAFT
	t_draft0 = time.perf_counter()
	msg = body.message.strip()
	if not msg:
		draft = "Input is empty; cannot analyze content."
	else:
		draft = f"Initial analysis of '{msg}' identifies key terms and required context for sound reasoning."
	t_draft1 = time.perf_counter()

	# REFLECT
	t_reflect0 = time.perf_counter()
	reflect_pts = _reflect_points(draft, msg)
	reflect = "\n".join(f"- {p}" for p in reflect_pts)
	t_reflect1 = time.perf_counter()

	# REVISE
	t_revise0 = time.perf_counter()
	if any("contradiction" in p.lower() for p in reflect_pts):
		revise = (
			"The prompt contains a possible contradiction or ambiguity. "
			"Clarify the conflicting terms or desired priority so the next step can be correct."
		)
	elif any("evidence" in p.lower() for p in reflect_pts):
		revise = (
			f"Building on the draft: {draft} We must reference concrete, verifiable sources "
			"and explicitly state assumptions to avoid overreach."
		)
	else:
		revise = (
			f"Improving the draft: {draft} We separate claims from evidence and list assumptions "
			"to enable a reliable conclusion."
		)
	t_revise1 = time.perf_counter()

	# LEARNED (rule)
	learned = "Structured reflection (claims vs evidence vs assumptions) reduces hidden contradictions."

	text = (
		f"DRAFT\n{draft}\n\n"
		f"REFLECT\n{reflect}\n\n"
		f"REVISE\n{revise}\n\n"
		f"LEARNED\n{learned}"
	)

	# Proof v2 (spec-aligned)
	run_id = _now_run_id()
	policy_str = "attention=bounded;cycles<=2;deterministic=true;eu_law_only=true"
	model_id = "ultra_simple_chat:1.0"
	proof = {
		"decision": "APPROVE",
		"cycles": min(max(body.max_cycles or 1, 0), 2),
		"audit_ref": run_id,
		"model_sha": f"sha256:{_sha256_hex(model_id)}",
		"policy_sha": f"sha256:{_sha256_hex(policy_str)}",
		"attention_state": (body.attention_state or "FAIR").upper(),
		"cr_event": {"old": "", "new": ""},
		"bus_msg_id": uuid.uuid4().hex,
		"sampler": sampler,
		"timings": {
			"draft_ms": int((t_draft1 - t_draft0) * 1000),
			"reflect_ms": int((t_reflect1 - t_reflect0) * 1000),
			"revise_ms": int((t_revise1 - t_revise0) * 1000),
			"total_ms": int((time.perf_counter() - t0) * 1000),
		},
	}

	return {"text": text, "pb2s_proof": proof}


if __name__ == "__main__":
	# Fallback runner (not recommended for production; prefer uvicorn CLI)
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8000)

