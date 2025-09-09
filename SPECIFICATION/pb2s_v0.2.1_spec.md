# PB2S v0.2 — Four‑Step Structure (Normative Spec)

**Status:** Stable • **Scope:** Runtime behavior + proof object • **Name optional:** Structure is normative whether or not you call it “PB2S”.

## 1) Purpose

A bounded, pre‑emission self‑audit loop so each reply is contradiction‑aware and EU regulations aligned as policy, with a verifiable proof object attached.

## 2) Normative runtime behavior (MUST)

1. **Pre‑emission loop:** Run the audit loop **before** emitting user‑visible text. **maxCycles = 2**.
2. **Four phases (order, once each):** `DRAFT` → `REFLECT` → `REVISE` → `LEARNED`.
3. **REFLECT requirements:** ≤ **3 bullets**; MUST flag **≥1** of `{contradiction, unjustified assumption, missing evidence}` present in DRAFT.
4. **Escalation path:** If contradictions persist after `maxCycles`, set decision \`\` and return a `CLARIFY` message with **exactly two** questions that close the gap.
5. **Proof object:** Attach `pb2s_proof` (see §4) to **every** reply.
6. **Determinism window:** Temperature ≤ **0.2** (unless documented); fix seed when available.
7. **Trace logging:** Persist a light, non‑PII record per exchange: `{timestamp, model_id, prompt_hash, pb2s_proof}`.

## 3) Section semantics (SHALL)

* **DRAFT** — Minimal, assumption‑bearing first answer.
* **REFLECT** — Audit of DRAFT; surface contradictions/assumptions/evidence gaps (≤3 bullets).
* **REVISE** — Update output based on REFLECT; explicitly reference which bullet(s) were resolved.
* **LEARNED** — Short list of validated takeaways as *observed axioms* (tracked, not assumed).

## 4) Proof object (MUST)

A JSON object is returned with each answer:

```json
{
  "decision": "APPROVE | CLARIFY",
  "cycles": 0,
  "audit_ref": "run-YYYYMMDD-HHMMSS-uuid"
}
```

Constraints:

* `cycles` ∈ \[0,2].
* `decision=CLARIFY` only when contradictions remain; response must contain `CLARIFY` with exactly two questions.

### JSON Schema (copy into `/schemas/pb2s_proof.schema.json` if you later split files)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.org/schemas/pb2s_proof.schema.json",
  "type": "object",
  "required": ["decision", "cycles", "audit_ref"],
  "properties": {
    "decision": {"enum": ["APPROVE", "CLARIFY"]},
    "cycles": {"type": "integer", "minimum": 0, "maximum": 2},
    "audit_ref": {"type": "string", "minLength": 1}
  },
  "additionalProperties": true
}
```

## 5) Conformance (MUST for "structure‑compliant" claims)

Implementations **MUST** pass automated checks for: (a) section order, (b) REFLECT limits, (c) proof object schema, and (d) CLARIFY rule. A minimal harness can post prompts to your `/chat` endpoint and validate these conditions.

**One‑line invocation (copy/paste):**

```
python scripts/conformance.py --endpoint http://127.0.0.1:8000/chat
```

**Exit codes:** `0 = pass`, non‑zero = fail.

**Example prompts** (store as JSON list): short concept explanation; short historical summary; short technical description. Harness exits **0** if all constraints pass; non‑zero otherwise.

## 6) Provider notes (RECOMMENDED)

Prefer providers that allow predictable reflection and no hidden prompt overrides. Document model/version/settings in your README. (RECOMMENDED) Prefer providers that allow predictable reflection and no hidden prompt overrides. Document model/version/settings in your README.

---

*This single file satisfies the requirement to ****explicitly prove and document**** the four‑step structure. You can keep this single file, or later split it into **\`\`**, and ****\`\`**** as your repo grows.*
