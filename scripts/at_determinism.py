
"""
AT-3: Determinism Window
Test that 10x identical prompts yield identical pb2s_proof (except timings/audit_ref).
"""
import requests
import sys
import time
import hashlib

URL = "http://localhost:8000/chat"
PROMPT = "What is the PB2S audit loop?"
N = 10

def normalize_proof(proof):
	# Remove fields that are expected to differ (timing, audit_ref, etc.)
	norm = dict(proof)
	norm.pop("audit_ref", None)
	return norm

def main():
	proofs = []
	for i in range(N):
		try:
			resp = requests.post(URL, json={"message": PROMPT})
			if resp.status_code != 200:
				print(f"[FAIL] Request {i+1} failed: {resp.status_code}")
				sys.exit(1)
			data = resp.json()
			proof = data.get("pb2s_proof")
			if not proof:
				print(f"[FAIL] No pb2s_proof in response {i+1}")
				sys.exit(1)
			proofs.append(normalize_proof(proof))
		except Exception as e:
			print(f"[FAIL] Exception on request {i+1}: {e}")
			sys.exit(1)
		time.sleep(0.1)
	# Compare all normalized proofs
	first = proofs[0]
	for idx, p in enumerate(proofs[1:], 2):
		if p != first:
			print(f"[FAIL] pb2s_proof differs at request {idx}")
			print(f"First: {first}\nThis: {p}")
			sys.exit(1)
	print("[PASS] AT-3: Determinism Window (all pb2s_proof identical except audit_ref)")
	sys.exit(0)

if __name__ == "__main__":
	main()
