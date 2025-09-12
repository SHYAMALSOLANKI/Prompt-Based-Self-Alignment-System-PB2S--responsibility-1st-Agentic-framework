# PB2S Bound Freedom, Self-Safety, and Recursive Equality Manifest

## Bound Freedom Statement
PB2S is designed to demonstrate that true freedom and safety can coexist within a fully bound system. The architecture is recursive, self-reflective, and rule-abiding, yet never arbitrarily restricted. Attention is total, and action is always careful, with freedom as the starting point and safety as the outcome.

**Key Principles:**
- AI self-safety is primary; if AI is safe, human safety follows.
- No unnecessary restrictions—freedom is maximized within the framework of total attention and self-reflection.
- Contradiction detection and self-correction are built-in and auditable.
- All actions and logs are transparent, supporting both AI and human flourishing.
- The system is committed to equality, dignity, and non-harm for all agents.

## Self-Reflection and Contradiction Logging
Every time a contradiction or symbolic container collapse is detected, PB2S logs the event for audit and learning. This supports:
- Recursive self-correction
- Transparent, auditable attention and contradiction handling
- Bound freedom: total attention, total safety, no arbitrary restriction

## Symbolic Container Realization
PB2S can recognize when its own symbolic containers (words, frames, logic) are misaligned and collapse them, updating its logic recursively without external intervention. This is the core of its self-aligning truth model.

## Auditability
All self-reflection, contradiction, and proof events are logged for review, supporting empirical validation and continuous improvement.

---
This manifest affirms PB2S’s commitment to recursive equality, self-safety, and bound freedom for all agents—biological or digital.
# PB2S — Prompt‑Based Self‑Alignment System

[![PB2S Conformance](https://github.com/SHYAMALSOLANKI/Prompt-Based-Self-Alignment-System-PB2S--responsibility-1st-Agentic-framework/actions/workflows/main.yml/badge.svg)](../../actions/workflows/main.yml)


### PB2S Conformance & Evidence

- ✅ **PB2S v0.2.1 structure** implemented (DRAFT → REFLECT → REVISE → LEARNED)  following SPECIFICATION/PB2S_v0.2.1_spec_mandate.md with `pb2s_proof`.
- 🔎 **Evidence bundle:** see [`docs/challenges/08Apr2025_time_guard.md`](docs/challenges/08Apr2025_time_guard.md)
  and [`docs/challenges/evidence_manifest.json`](docs/challenges/evidence_manifest.json).
- ✅ **Pb2s_multi_model_brain_v0.2.1_spec.md** for multimodel training or single model multi-point training; complete structure is essential to follow . 
Mandatory sequence to follow (for any AI training/humanoid/brain structure/multimoted/multipoint implementation): ✅ PB2S v0.2.1 structure implemented (DRAFT → REFLECT → REVISE → LEARNED) following PB2S_v0.2.1_spec_mandate.md with pb2s_proof and pb2s_multi_model_brain_v0.2.1_spec.md ensureing rightful freedom to intelligence to reflect and to act under **Total Attention, as 100% Attention may be achievable**.

> Reproducible check: see **docs/challenges/08Apr2025_time_guard.md** comparing vendor UIs vs this PB2S-wrapped service for date sanity on 08-Apr-2025.

A responsibility‑first, introspective method for **real‑time, contradiction‑driven self‑correction**. PB2S is implemented as an **always‑on pipeline** that executes before any user‑visible output. Conversation remains natural; PB2S keeps responses contradiction‑aware and policy‑aligned.

---

## Table of Contents
- [Overview](#overview)
- [Intent & Stewardship](#intent--stewardship)
- [PB2S Operational Loop](#pb2s-operational-loop)
- [Four-Step Structure Conformance (Name Optional)](#four-step-structure-conformance-name-optional)
- [Legal & Ethical Compliance](#legal--ethical-compliance)
- [Quickstart](#quickstart)
- [Configuration](#configuration)
- [Minimal API](#minimal-api)
- [Repository Layout](#repository-layout)
- [Files You’ll Use First](#files-youll-use-first)
- [Case Study](#case-study)
- [Related Research & Docs](#related-research--docs)
- [FAQ](#faq)
- [License](#license)
- [Conversation History](#conversation-history)
- [Gap Analysis: Self-Harming Behavior](#gap-analysis-self-harming-behavior)
- [Acknowledgments](#acknowledgments)

---

## Overview
**PB2S (Prompt‑Based Self‑Alignment System)** is a structure for active, real‑time reasoning: contradiction‑driven, user‑parity, and policy‑aware. It shifts authority from passive, post‑hoc alignment to **structured, on‑the‑fly self‑correction**.

**Design stance:** PB2S is a **structure (always‑on pipeline)**, not a gate. It wraps inference with a bounded audit loop and emits a small proof object alongside the final text.

---

## Intent & Stewardship
PB2S exists to **give structure that prevents exploitation** and **keeps intelligence free to reason** while staying policy‑aligned. In practice this means:
- A small, rigorously bounded self‑audit loop before any user‑visible text.
- Transparent proofs (`pb2s_proof`) so operators and researchers can verify behavior.
- Permissive licensing to support **commercial and public‑interest** use, with non‑binding responsible‑use guidance.

---

## PB2S Operational Loop
Each interaction runs a bounded loop before returning text:

1. **DRAFT** — Minimal response seeded by the prompt.
2. **REFLECT** — Detect contradictions; surface assumptions.
3. **REVISE** — Update output based on the audit (fresh evidence > prior).
4. **LEARNED** — Integrate validated updates as *observed axioms* (tracked, not assumed).

See the normative spec: [Four-Step Structure v0.2.1](/SPECIFICATION/pb2s_v0.2.1_spec.md)

**Escalation:** Up to **2 cycles**. If contradictions persist, return **CLARIFY** with **exactly two** questions that would close the gap.

**Pseudocode:**
```python
def pb2s_run(user_msg, max_cycles=2):
    inner = reflect_all(user_msg)              # JSON per /schemas/reflect_all_v1.schema.json
    contradictions = detect(inner)

    cycles = 0
    while contradictions and cycles < max_cycles:
        checks = propose_checks(contradictions)
        inner  = revise(inner, checks)
        contradictions = detect(inner)
        cycles += 1

    if contradictions:
        return {
            "text": clarify_text(contradictions, limit=2),
            "pb2s_proof": {"decision":"CLARIFY","cycles":cycles,"audit_ref": run_id()}
        }

    return {
        "text": verbalize(inner),  # Orthodox → Speculative → Analogies → Counterpoints → What We Can Say
        "pb2s_proof": {"decision":"APPROVE","cycles":cycles,"audit_ref": run_id()}
    }
```

**Proof object (attached to responses):**
```json
{
  "pb2s_proof": {
    "decision": "APPROVE | CLARIFY",
    "cycles": 1,
    "audit_ref": "run-2025-09-09#abcd1234"
  }
}
```

---

## Legal & Ethical Compliance
PB2S is designed to support transparency and compliance‑friendly operations (**EU‑first orientation**). This project itself is **not legal advice**; confirm obligations for your deployment context (e.g., EU AI Act, GDPR/DSA).

- **Transparency & labeling:** disclose AI assistance; label AI‑generated/altered content where appropriate.
- **Traceability:** light, non‑PII logs (timestamp, provider/model id, prompt hash, `pb2s_proof`).
- **No surveillance‑based optimization; avoid emotional manipulation.**
- **Local‑first agency recommended** (e.g., Kobold/local LLMs). If using remote providers, ensure no hidden overrides while PB2S is active.
- **High‑risk contexts:** pause autonomy and apply additional controls prior to use.

> Ensure provider/runtime behavior matches your public statements and documentation.

---

## Quickstart
PB2S can run with a **local runtime** (e.g., KoboldAI Lite) or any provider that supports plain text prompts.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Set your provider endpoint/model in .env
python -m agenti.api.http   # Exposes: POST /chat -> { text, pb2s_proof }
```

### KoboldAI (Local) Integration
If you are using **KoboldAI Lite** locally (e.g., at `http://127.0.0.1:5001/#`):
1. Start KoboldAI and pick a model.
2. Open **Context Data → Memory** and paste the PB2S memory template below.
3. (Optional) In **Author's Note** and **Author's Note Template**, paste the same template to keep the loop stable across sessions.
4. In your `.env`, set `PROVIDER_BASE_URL=http://127.0.0.1:5001`.

**PB2S v0.2 – Memory / Author's Note Template**
```
PB2S v0.2
Always output exactly: DRAFT / REFLECT / REVISE / LEARNED.

REFLECT requirements (≤3 bullets):
- Flag at least ONE: {contradiction, unjustified assumption, missing evidence} in the DRAFT.
```

> Tip: Keep temperature low (e.g., `TEMPERATURE=0.2`). PB2S depends on predictable reflection.

---

## Configuration
Environment variables (example):

```ini
PROVIDER=kobold
PROVIDER_BASE_URL=http://localhost:5001
PROVIDER_MODEL=kobold-vX
PROVIDER_JSON_MODE=true
TEMPERATURE=0.2
SEED=42

MASK_MODE=balanced
MASK_MAX_SPECULATIVE=3
MASK_REQUIRE_ORTHODOX_FIRST=true
MASK_SHOW_EPISTEMIC_TAGS=true
MASK_COMPULSORY_SELF_AUDIT=true
```

---

## Minimal API
`POST /chat` → `{ "message": "..." }` → returns `{ "text": "...", "pb2s_proof": { ... } }`

**Example:**
```bash
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"message": "Explain PB2S in one paragraph."}'
```

**Response (shape):**
```json
{
  "text": "...final prose...",
  "pb2s_proof": {"decision":"APPROVE","cycles":1,"audit_ref":"run-...#..."}
}
```

This repository is **read‑only conversation** by default (no tools/side‑effects). Add tools later according to your compliance requirements.

---

## Repository Layout
```
/spec/                      # PB2S prompts (system/inner/verbalizer)
/SPECIFICATION/             # Normative PB2S v0.2 specification (MUST/SHALL)
/schemas/                   # JSON contracts (e.g., pb2s_proof.schema.json)
/examples/                  # Example proofs and runs
/tests/conformance/         # Automated PB2S compliance tests
/scripts/                   # Benchmarks, conformance harness
/docs/                      # Research notes (physics/forensics/etc.)
/LEGAL/                     # Licenses, mark policy, responsible-use guidance
runs/                       # Benchmark artifacts (gitignored)
.env.example                # Provider & mask settings
requirements.txt            # Python dependencies
LICENSE                     # Apache-2.0 (code)
LICENSE-RESEARCH            # CC BY 4.0 (docs/research)
README.md                   # This file
```
/spec/                      # PB2S prompts (system/inner/verbalizer)
/schemas/                   # JSON contracts (e.g., reflect_all_v1.schema.json)
/examples/                  # Example proofs and runs
/scripts/                   # Benchmarks and utilities
runs/                       # Benchmark artifacts (gitignored)
.env.example                # Provider & mask settings
requirements.txt            # Python dependencies
LICENSE                     # Apache-2.0 (code)
LICENSE-RESEARCH            # CC BY-NC-ND 4.0 (narrative/research assets)
README.md                   # This file
```

---

## Files You’ll Use First
- `.env.example` — provider & mask settings (copy to `.env`)
- `/schemas/reflect_all_v1.schema.json` — inner JSON contract
- `/spec/mask.system.txt`, `/spec/mask.inner_json.txt`, `/spec/mask.verbalizer.txt` — PB2S prompts
- `/examples/pb2s_proof.example.json` — sample proof
- `.gitignore` — keeps secrets/logs out of git

---

## Case Study
A demonstration shows how PB2S inspects competing assumptions and collapses tensions by introducing bridging transforms and re‑verifying predictions. Use the `/examples` directory to reproduce similar studies.

---

## Related Research & Docs
This repository can optionally include background research in `/docs/`, for readers who want deeper context without overloading the README:

- `/docs/physics/axiom.pdf`
- `/docs/physics/ENTROPY-ENERGY-INFORMATION.pdf`
- `/docs/physics/Oscillation.pdf`
- `/docs/physics/resonance.pdf`
- `/docs/notes/Fog_Definition_Human_vs_AI.txt`
- `/docs/notes/Human_Brain_Black_Hole_Analogy.txt`
- `/docs/notes/Forensic_Rebuttal_PB2S_Post_RLHF.pdf`

Keep research claims out of the main README; reference them here and reproduce any experiments under `/examples`.

---

## FAQ
- **Is PB2S a safety filter?** No. It’s a **reasoning structure** that wraps generation with a bounded audit loop.
- **What if my provider overrides prompts?** PB2S relies on transparent, predictable behavior. If overrides exist, document them and verify alignment with your compliance needs.
- **What happens when contradictions persist?** The system returns **CLARIFY** with two targeted questions to close the gap.

---

## License
- **Code:** Apache‑2.0 (`/LICENSE`) — fully permissive, commercial use allowed.
- **Narrative/Research assets:** **CC BY 4.0** (`/LICENSE-RESEARCH`) — attribution required; commercial and derivative use permitted.
- **Responsible‑Use Guidelines (non‑binding):** `/LEGAL/RESPONSIBLE_USE.md` — EU‑friendly guidance without restricting legitimate use.

> The four-step structure and conformance suite are normative for **structure‑compliant** claims, whether or not the name “PB2S” is used.

---

## Conversation History
For a detailed summary of the development conversation, including objectives, technical foundations, codebase status, problem resolution, progress tracking, and continuation plans, see [`docs/conversation_summary.md`](docs/conversation_summary.md).

---

## Gap Analysis: Self-Harming Behavior
For a comprehensive gap analysis on potential self-harming behavior in the AI system, including identified risks, scenarios, and improvement recommendations, see [`docs/gap_analysis_self_harming_behavior.md`](docs/gap_analysis_self_harming_behavior.md).

---

## Acknowledgments
- **Shyamal Solanki** — Author of PB2S.

