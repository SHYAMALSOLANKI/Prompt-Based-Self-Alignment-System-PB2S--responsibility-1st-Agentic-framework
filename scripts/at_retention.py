
"""
AT-7: Retention & Hashing
Test that policy exists and sample artifacts contain SHA-256 fields.
"""
import os
import sys
import json

POLICY_PATH = "infra/systemd/attention.service.d/10-rt.conf"  # Example policy file
ARTIFACT_PATHS = ["pb2s_trace.log"]  # Add more artifact paths as needed

def check_policy():
	if not os.path.exists(POLICY_PATH):
		print(f"[FAIL] Policy file missing: {POLICY_PATH}")
		return False
	print(f"[PASS] Policy file exists: {POLICY_PATH}")
	return True

def check_sha256_in_artifacts():
	found = False
	for path in ARTIFACT_PATHS:
		if not os.path.exists(path):
			print(f"[WARN] Artifact missing: {path}")
			continue
		with open(path, "r", encoding="utf-8") as f:
			for line in f:
				if 'sha256' in line or 'SHA-256' in line:
					found = True
					break
	if found:
		print("[PASS] SHA-256 field found in artifacts")
		return True
	else:
		print("[FAIL] No SHA-256 field found in artifacts")
		return False

def main():
	ok = check_policy() and check_sha256_in_artifacts()
	if ok:
		print("[PASS] AT-7: Retention & Hashing")
		sys.exit(0)
	else:
		print("[FAIL] AT-7: Retention & Hashing")
		sys.exit(1)

if __name__ == "__main__":
	main()
