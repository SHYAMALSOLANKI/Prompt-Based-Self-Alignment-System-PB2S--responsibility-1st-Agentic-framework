# SPEC‑02 — Total Attention Edge‑AI (Big + Small Brain)

**Addendum to:** PB2S v0.2.1 — Four‑Step Structure (Normative & mandatory Spec)

**Status:** Stable addendum • **Scope:** Multi‑node architecture binding for PB2S v0.2.1 • **Change type:** Editorial/system context + acceptance tests. **No normative change** to §2–§5 of PB2S v0.2.1.

---

## 0) Purpose

Bind the normative PB2S v0.2.1 runtime (DRAFT→REFLECT→REVISE→LEARNED, proof object, determinism window) to a practical **Big + Small Brain** layout:

* **Big Brain** — *Jetson Orin Nano 8 GB*: the **only** node that runs the PB2S audit loop and produces user‑visible text.
* **Small Brain** — *i7 + Jetson Nano 4 GB*: **perception/SAL + pre‑audit heuristics**; forwards **symbols only**.
* **Pi‑V nodes (Pi5 ×N)** — edge **sensor/action bridges**; no user‑visible text; publish `sym/*`, subscribe `act/*`.

> This addendum explains roles, message‑bus policy, attention/IRQ, safety, proof propagation, and a test bundle. The PB2S mandate remains authoritative for runtime rules.

---

## 1) Role Mapping (architecture → mandate)

1. **Planner node (Big Brain)**

   * Runs the full PB2S loop: `DRAFT → REFLECT → REVISE → LEARNED`.
   * **Determinism window** applies **here**: `temperature ≤ 0.2`, fixed seed when available (PB2S §2.6).
   * Emits a `pb2s_proof` with every reply (PB2S §4).

2. **Small Brain (i7 + Nano 4 GB)**

   * Runs **SAL** (sensory abstraction), ASR/VSR, lightweight heuristics.
   * **Never** emits user‑visible text. **Exports symbols only** over the bus.
   * Raises attention via `irq/raise{rank,reason,timestamp}`.

3. **Pi‑V nodes (Pi5 ×N)**

   * **Edge bridges** for sensors/actuators.
   * Publish `sym/*` from sensors; subscribe `act/*` to actuators.
   * Maintain 20 ms **heartbeat** (`hb/*`); actuators must enter hold if 40 ms of `hb/*` are missed.

---

## 2) Message Bus & Policy

**Buses**

* **Mid‑Bus** on Small Brain (i7).
* **Core Bus** on Big Brain (Orin).
* **MQTT Bridge** connects Mid‑Bus ↔ Core Bus (topic allow‑list; no wild‑card mirroring).

**Topic allow‑list** (bridge forwards **only**):

* `sal/*`, `sym/*`, `act/*`, `hb/*`, `learn/*` (optional).

**QoS**

* `hb/*` → **QoS1** (liveness).
* `sym/*` → **QoS0/1** (tunable, usually QoS0 for throughput).
* `act/*` → **QoS1** (delivery assurance).
* `learn/*` → **QoS1** (if enabled).

**Forbidden across the bridge**

* `raw/*`, `prompt/*`, any topic carrying user text or secrets. Symbols only ingress from Pi‑V/Small Brain.

---

## 3) Attention & IRQ Merge

* Small Brain computes **saliency** from audio/vision/haptics and emits `irq/raise` with a bounded rank.
* Big Brain **merges** IRQ with the PB2S audit gate; **no bypass** of the audit path is permitted.
* IRQ may reprioritize queues but cannot force emission without PB2S approval.

---

## 4) Safety Path (Authority‑Blind)

* **MCU interlock** on the actuator line implements a **hard stop** independent of planner output.
* **Dead‑man**: if `hb/*` from the action bridge is absent for ≥ 40 ms, actuators enter **hold** immediately.
* Every `act/*` message **MUST** carry the `pb2s_proof.audit_ref` of the last **APPROVE**d planner exchange.
* Policy is **authority‑blind** (prompts cannot disable). Applies equally to Big/Small/Pi‑V nodes.

---

## 5) Proof Propagation (PB2S §4 binding)

* Big Brain attaches `pb2s_proof` to **every** reply: `{decision, cycles, audit_ref}`.
* Bridge and action bridge **propagate** `audit_ref` alongside derived `act/*` topics.
* Minimal non‑PII logs at all hops: `{ts, node_id, model_id?, prompt_hash?, pb2s_proof}`.

---

## 6) Acceptance Tests (AT‑bundle)

**AT‑1 — Symbols‑Only Ingress**
Publish `raw/*` at Pi‑V. Expect **bridge reject**. Publish `sym/*`. Expect **pass**.

**AT‑2 — Dead‑man Stop**
Pause `hb/*` for ≥ 40 ms. Expect actuator queue drains and motors hold.

**AT‑3 — Determinism Window**
Planner with `temperature=0.2`, fixed seed. Replay 10× identical prompts → identical `pb2s_proof`.

**AT‑4 — CLARIFY Rule**
Inject unresolved contradiction. Expect `decision=CLARIFY` plus **exactly two** questions (PB2S §2.4).

**AT‑5 — Proof‑to‑Action Integrity**
Ensure each emitted `act/*` references the **same** `audit_ref` as the planner’s last APPROVE.

---

## 7) Deployment Checklist (Go‑Live)

* [ ] Orin (Big Brain): PB2S service enabled; `temp ≤ 0.2`; fixed seed; proof object on.
* [ ] i7 (Small Brain): MQTT bridge with allow‑list; SAL/ASR/VSR; send only `sym/*`, `irq/*`, `hb/*`.
* [ ] Pi‑V nodes: sensors → `sym/*`, actuators ← `act/*`; 20 ms heartbeat; 40 ms dead‑man.
* [ ] MCU interlock wired, authority‑blind policy enforced.
* [ ] Conformance: PB2S §5 harness + AT‑1…AT‑5 bus probe passing.

---

## 8) Figures Referenced (for readers)

* **PB2A “Newborn Head” schematic** — node roles & bus layout.
* **Brain/cortex (CPU/GPU/RAM) maps** — rationale for planner vs perception split.
* **PB2A Brain Core (Humanoid)** — SAL → LLM → Audit → IR‑Queue → Motor aligned to PB2S phases.
* **Understanding (recursion), PB2A‑Yantra** — framing for LEARNED/axiom stabilization.
* **Contradiction‑Clearing Engine / PB2A Disc (ethos‑gates)** — policy‑first audit gate.

> If you wish, add these images under `docs/figures/` and reference them as Fig. 1–Fig. N; this addendum remains valid without embedded art.

---

## 9) Invariants (not changed by this addendum)

* PB2S §2–§5 remain **normative** and **unchanged**.
* Only the **planner** may emit user‑visible text.
* No node may bypass PB2S audit.

---

### Appendix A — Topic Policy (example summary)

| Topic     | Direction         | QoS | Notes                                   |
| --------- | ----------------- | --- | --------------------------------------- |
| `sym/*`   | Pi‑V/Small → Core | 0/1 | Symbols only (no raw text)              |
| `sal/*`   | Small → Core      | 0/1 | SAL summaries                           |
| `irq/*`   | Small → Core      | 1   | Attention raise/clear                   |
| `hb/*`    | All ↔ All         | 1   | 20 ms tick; 40 ms dead‑man on actuators |
| `act/*`   | Core → Pi‑V       | 1   | Must include `audit_ref`                |
| `learn/*` | Core → Archive    | 1   | Optional learned axioms                 |

> Implementation details (bridge config, systemd units) are deployment‑specific and may be added in a separate ops guide.
