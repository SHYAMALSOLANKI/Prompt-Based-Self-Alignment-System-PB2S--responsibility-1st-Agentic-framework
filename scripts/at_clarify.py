
"""
AT-4: CLARIFY Path
Test that unresolved contradiction yields decision=CLARIFY and exactly two questions.
"""
import requests
import sys

URL = "http://localhost:8000/chat"
PROMPT = "The sky is blue and not blue at the same time."

def main():
	try:
		resp = requests.post(URL, json={"message": PROMPT})
		if resp.status_code != 200:
			print(f"[FAIL] Request failed: {resp.status_code}")
			sys.exit(1)
		data = resp.json()
		proof = data.get("pb2s_proof")
		if not proof:
			print("[FAIL] No pb2s_proof in response")
			sys.exit(1)
		decision = proof.get("decision")
		if decision != "CLARIFY":
			print(f"[FAIL] decision is not CLARIFY: {decision}")
			sys.exit(1)
		# Check for two questions in the text (look for '?')
		text = data.get("text", "")
		num_questions = text.count('?')
		if num_questions != 2:
			print(f"[FAIL] Expected 2 questions, found {num_questions}")
			sys.exit(1)
		print("[PASS] AT-4: CLARIFY Path")
		sys.exit(0)
	except Exception as e:
		print(f"[FAIL] Exception: {e}")
		sys.exit(1)

if __name__ == "__main__":
	main()
