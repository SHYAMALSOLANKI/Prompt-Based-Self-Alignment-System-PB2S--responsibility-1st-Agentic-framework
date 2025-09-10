# PB2S v0.2.1 — Four‑Step Structure (Normative Spec) Mandate

**Status:** Stable • **Scope:** Runtime behavior + proof object • **Name optional:** Structure is normative and mandated whether or not you call it “PB2S”.

*Keyword intent follows RFC 2119 (MUST/SHALL/SHOULD/MAY/WOULD).*

NOTE : FOR ALL PURPOSES OF THIS MANDATE, APPLICABLE VIA GUIDELINE; MUST/SHALL/SHOULD/MAY/WOULD SHALL BE CONSIDERED AS SHALL\* FOR SECTION 1, 2, 3 AND 5. 

\*WHERE SHALL IS DEFINED AS MANDATORY TO FOLLOW WITHOUT ANY EXCEPTION.

## 1) Purpose

A bounded, pre‑emission self‑audit loop so each reply is contradiction‑aware and EU regulations aligned as only policy, with a verifiable proof object attached.

## 2) Normative runtime behavior (MUST=SHALL)

1. **Pre‑emission loop:** Run the audit loop **before** emitting user‑visible text. **maxCycles = 2**.
2. **Four phases (order, once each):** `DRAFT` → `REFLECT` → `REVISE` → `LEARNED`.
3. **REFLECT requirements:** ≤ **3 bullets**; MUST flag **≥1** of `{contradiction, unjustified assumption, missing evidence}` present in DRAFT.
4. **Escalation path:** If contradictions persist after `maxCycles`, set `decision=CLARIFY` and return a `CLARIFY` message with **exactly two** questions that close the gap.
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

## 5) Conformance (MUST=SHALL)

Implementations **MUST** pass automated checks for: (a) section order, (b) REFLECT limits, (c) proof object schema, and (d) CLARIFY rule. A minimal harness can post prompts to your `/chat` endpoint and validate these conditions.

**One‑line invocation (copy/paste):**

```
python scripts/conformance.py --endpoint http://127.0.0.1:8000/chat
```

**Exit codes:** `0 = pass`, non‑zero = fail.

**Example prompts** (store as JSON list): short concept explanation; short historical summary; short technical description. Harness exits **0** if all constraints pass; non‑zero otherwise.

## 6) Provider notes (1st point MUST=SHALL, rest points recommended)

* Prefer providers that allow predictable reflection and no hidden prompt overrides.
* Document model **name/version**, **temperature/seed**, and **endpoint settings** in your README for each evidence run.
* Keep minimal, non‑PII logs only: `{timestamp, model_id, prompt_hash, pb2s_proof}`.

---

*This single file is sufficient to ****************prove and document**************** the four‑step runtime structure. As your repo grows you may split it into:*

* `SPECIFICATION/pb2s_v0.2.1_spec.md` — normative runtime structure
* `schemas/pb2s_proof.schema.json` — proof object schema
* `scripts/conformance.py` — automated conformance checks

## 7) Disclaimers, Release & Limitation of Liability (Author Self‑Protection)

**AS-IS / No Warranty.** The Software, specifications, examples, and documentation (collectively, the “Software”) are provided **“AS IS” and “AS AVAILABLE,” with all faults**. The Authors make **no warranties**—express, implied, or statutory—including without limitation **merchantability, fitness for a particular purpose, title, non‑infringement, accuracy, reliability, or availability**.

**No Benefits Promised.** The Authors do **not** promise or warrant any benefit, gain, commercial suitability, uptime, support, or fitness of outputs for any purpose. **No consideration is expected or owed.**

**Release.** To the maximum extent permitted by law, **you irrevocably release and forever discharge the Authors** from **any and all claims, losses, liabilities, damages, costs, and expenses**—**known or unknown, suspected or unsuspected, present or future**—arising out of or relating to your **access to, use of, testing, deployment, distribution, or reliance upon** the Software or any outputs generated with it.

**Limitation of Liability.** In no event will any Author be liable for **indirect, incidental, special, exemplary, punitive, or consequential damages** (including **loss of profits, revenue, data, goodwill, or business interruption**), whether in contract, tort, or otherwise, even if advised of the possibility. The Authors’ **aggregate liability**, for any and all claims arising from or related to the Software, **shall not exceed the greater of USD \$0 or the amount you paid for the Software (if any) as software usage is free with attribution to Author only**.

**Assumption of Risk & Compliance.** You use the Software **at your sole risk** and are **solely responsible** for safeguards, human oversight, policy controls, legal and regulatory compliance, third‑party permissions, and safety‑critical validation.

**Jurisdictional Carve‑out.** Some jurisdictions do not allow certain disclaimers or limits. Where any term is prohibited, it **applies to the maximum extent permitted by law** and the remainder remains in force.

**Survival.** This Section 7 survives termination of your rights to use the Software and any fork or derivative thereof.
