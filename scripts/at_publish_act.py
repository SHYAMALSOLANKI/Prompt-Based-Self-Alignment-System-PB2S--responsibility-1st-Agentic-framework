"""
Minimal act/* publisher for AT-5 test harness.
Publishes an act/test message with the latest audit_ref from pb2s_trace.log.
"""
import json
import time
from paho.mqtt import client as mqtt

MQTT_HOST = "127.0.0.1"
MQTT_PORT = 1883
ACT_TOPIC = "act/test"
TRACE_LOG = "pb2s_trace.log"

# Get the latest APPROVE audit_ref from the trace log
latest_audit_ref = None
try:
    with open(TRACE_LOG, "r", encoding="utf-8") as f:
        for line in reversed(f.readlines()):
            entry = json.loads(line)
            proof = entry.get("pb2s_proof", {})
            if proof.get("decision") == "APPROVE":
                latest_audit_ref = proof.get("audit_ref")
                break
except Exception:
    pass

if not latest_audit_ref:
    print("[FAIL] No APPROVE audit_ref found in trace log. Run /chat endpoint first.")
    exit(1)

payload = json.dumps({"audit_ref": latest_audit_ref, "action": "test_action"})

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_start()
result = client.publish(ACT_TOPIC, payload=payload, qos=0)
time.sleep(1)
client.loop_stop()
client.disconnect()
print(f"[PASS] Published act/* message with audit_ref: {latest_audit_ref}")
