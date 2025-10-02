
"""
AT-5: Proof-to-Action Integrity
Test that each act/* message references the same audit_ref as the planner's last APPROVE.
"""

import sys
import time
import json
from paho.mqtt import client as mqtt

MQTT_PROTOCOL = mqtt.MQTTv311

MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883
ACT_TOPIC = "act/#"
TRACE_LOG = "pb2s_trace.log"
TIMEOUT = 5

def get_last_approve_audit_ref():
	try:
		with open(TRACE_LOG, "r", encoding="utf-8") as f:
			for line in reversed(f.readlines()):
				entry = json.loads(line)
				proof = entry.get("pb2s_proof", {})
				if proof.get("decision") == "APPROVE":
					return proof.get("audit_ref")
	except Exception:
		pass
	return None

def main():
	last_audit_ref = get_last_approve_audit_ref()
	if not last_audit_ref:
		print("[FAIL] No APPROVE audit_ref found in trace log")
		sys.exit(1)
	found = False
	def on_message(client, userdata, msg):
		nonlocal found
		try:
			payload = msg.payload.decode("utf-8")
			data = json.loads(payload)
			audit_ref = data.get("audit_ref")
			if audit_ref == last_audit_ref:
				print("[PASS] AT-5: Proof-to-Action Integrity")
				found = True
				client.disconnect()
		except Exception:
			pass

	client = mqtt.Client(protocol=MQTT_PROTOCOL)
	client.on_message = on_message
	try:
		client.connect(MQTT_HOST, MQTT_PORT, 60)
		client.subscribe(ACT_TOPIC)
		client.loop_start()
		t0 = time.time()
		while not found and (time.time() - t0 < TIMEOUT):
			time.sleep(0.2)
		client.loop_stop()
		client.disconnect()
		if not found:
			print("[FAIL] No act/* message with correct audit_ref received")
			sys.exit(1)
	except Exception as e:
		print(f"[FAIL] MQTT error: {e}")
		sys.exit(1)

if __name__ == "__main__":
	main()
