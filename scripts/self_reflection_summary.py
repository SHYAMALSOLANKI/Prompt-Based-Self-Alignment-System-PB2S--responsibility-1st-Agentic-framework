"""
Summarize all self-reflection and contradiction events from pb2s_self_reflection.log for audit and learning.
"""
import json

log_path = "pb2s_self_reflection.log"
try:
    with open(log_path, "r", encoding="utf-8") as f:
        events = [json.loads(line) for line in f if line.strip()]
except Exception:
    print("[WARN] No self-reflection log found.")
    events = []

if not events:
    print("[INFO] No self-reflection or contradiction events recorded yet.")
    exit(0)

print(f"[SUMMARY] {len(events)} self-reflection/contradiction events found:\n")
by_type = {}
for e in events:
    t = e.get("event", "unknown")
    by_type.setdefault(t, 0)
    by_type[t] += 1
for t, n in by_type.items():
    print(f"- {t}: {n}")

print("\nRecent events:")
for e in events[-10:]:
    print(json.dumps(e, indent=2))
