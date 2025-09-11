"""
Audit PB2S logs for unresolved contradictions, repeated container collapses, or foggy/ambiguous prompts.
"""
import json
import re

log_path = "pb2s_self_reflection.log"
try:
    with open(log_path, "r", encoding="utf-8") as f:
        events = [json.loads(line) for line in f if line.strip()]
except Exception:
    print("[WARN] No self-reflection log found.")
    events = []

unresolved = [e for e in events if e.get("event") == "contradiction_detected" and 'clarify' in e.get('draft', '').lower()]
repeats = {}
foggy = []
for e in events:
    prompt = e.get("prompt", "")
    if prompt:
        repeats[prompt] = repeats.get(prompt, 0) + 1
        if re.search(r"fog|unclear|ambiguous|vague", prompt, re.I):
            foggy.append(e)

print(f"[AUDIT] Unresolved contradictions: {len(unresolved)}")
for e in unresolved[-5:]:
    print(json.dumps(e, indent=2))
print(f"\nRepeated prompts (possible stuck loop):")
for p, n in repeats.items():
    if n > 1:
        print(f"- '{p}': {n} times")
print(f"\nFoggy/ambiguous prompts: {len(foggy)}")
for e in foggy[-5:]:
    print(json.dumps(e, indent=2))
