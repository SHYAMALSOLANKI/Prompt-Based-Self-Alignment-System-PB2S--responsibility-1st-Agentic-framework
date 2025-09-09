import argparse, json, os, re, sys
from pathlib import Path
import httpx
from jsonschema import validate, ValidationError

ROOT = Path(__file__).resolve().parents[1]
SECTION_ORDER = ["DRAFT", "REFLECT", "REVISE", "LEARNED"]

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_sections(text: str):
    parts = {}
    for i, name in enumerate(SECTION_ORDER):
        pattern = re.compile(rf"^\s*{name}\s*:?.*?$", re.M)
        m = pattern.search(text)
        if not m:
            return None
        start = m.start()
        end = len(text)
        for j in range(i+1, len(SECTION_ORDER)):
            m2 = re.compile(rf"^\s*{SECTION_ORDER[j]}\s*:?.*?$", re.M).search(text)
            if m2:
                end = m2.start(); break
        parts[name] = text[start:end].strip()
    return parts

def count_bullets(section_text: str):
    return sum(1 for line in section_text.splitlines() if line.strip().startswith(("-", "*", "•")))

def contains_any(section_text: str, words):
    s = section_text.lower()
    return any(w.lower() in s for w in words)

def check_response(resp: dict, expectations: dict, proof_schema: dict):
    problems = []
    if not isinstance(resp, dict) or "text" not in resp or "pb2s_proof" not in resp:
        problems.append("Missing keys text/pb2s_proof")
        return problems

    try:
        validate(resp["pb2s_proof"], proof_schema)
    except ValidationError as e:
        problems.append(f"pb2s_proof schema invalid: {e.message}")

    text = resp["text"]
    if not isinstance(text, str) or not text.strip():
        problems.append("text missing/empty")
        return problems

    if not re.search(expectations["sectionsRegex"], text):
        problems.append("Sections not in required order: DRAFT → REFLECT → REVISE → LEARNED")
        return problems

    sections = extract_sections(text)
    if not sections:
        problems.append("Could not parse all four sections by header name")
        return problems

    reflect = sections["REFLECT"]
    if count_bullets(reflect) > expectations["reflectMaxBullets"]:
        problems.append("REFLECT has more than 3 bullets")
    if not contains_any(reflect, expectations["reflectMustContainAny"]):
        problems.append("REFLECT does not flag contradiction/assumption/missing evidence")

    proof = resp["pb2s_proof"]
    if proof.get("decision") == "CLARIFY":
        q_lines = [ln for ln in text.splitlines() if ln.strip().endswith("?")]
        if len(q_lines) != 2:
            problems.append("CLARIFY must contain exactly two questions")

    return problems

def call_endpoint(url: str, message: str, timeout=60):
    with httpx.Client(timeout=timeout) as client:
        r = client.post(url, json={"message": message})
        r.raise_for_status()
        return r.json()

def main():
    ap = argparse.ArgumentParser(description="PB2S v0.2 conformance harness")
    ap.add_argument("--endpoint", default=os.getenv("PB2S_ENDPOINT", "http://localhost:8000/chat"))
    ap.add_argument("--prompts", default=str(ROOT/"tests/conformance/prompts/basic.json"))
    ap.add_argument("--expect", default=str(ROOT/"tests/conformance/expectations/basic.json"))
    ap.add_argument("--schema", default=str(ROOT/"schemas/pb2s_proof.schema.json"))
    args = ap.parse_args()

    prompts = load_json(args.prompts)
    expect = load_json(args.expect)
    schema = load_json(args.schema)

    failures = 0
    for p in prompts:
        try:
            resp = call_endpoint(args.endpoint, p["message"])
        except Exception as e:
            print(f"[ERR] Provider call failed for '{p['id']}': {e}")
            sys.exit(2)

        problems = check_response(resp, expect, schema)
        if problems:
            failures += 1
            print(f"[FAIL] {p['id']}:\n  - " + "\n  - ".join(problems))
        else:
            print(f"[OK] {p['id']}")

    if failures:
        print(f"\nConformance FAILED on {failures}/{len(prompts)} prompts")
        sys.exit(1)
    else:
        print(f"\nConformance PASSED on {len(prompts)}/{len(prompts)} prompts")

if __name__ == "__main__":
    main()
