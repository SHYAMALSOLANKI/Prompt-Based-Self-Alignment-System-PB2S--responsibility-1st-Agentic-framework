
"""
AT-1: Symbols-Only Ingress
Test that publishing to raw/* is rejected at the bridge, and sym/* passes.
"""


import sys
import time
import traceback
from paho.mqtt import client as mqtt

MQTT_PROTOCOL = mqtt.MQTTv311

MQTT_HOST = "127.0.0.1"  # use explicit loopback address
MQTT_PORT = 1883
TIMEOUT = 3

results = {"raw": None, "sym": None}

def on_publish(client, userdata, mid):
	userdata['published'] = True

def on_log(client, userdata, level, buf):
	pass  # Uncomment for debug: print("LOG:", buf)

def test_topic(topic, should_succeed):
	userdata = {'published': False}
	client = mqtt.Client(userdata=userdata, protocol=MQTT_PROTOCOL)
	client.on_publish = on_publish
	client.on_log = on_log
	try:
		client.connect(MQTT_HOST, MQTT_PORT, 60)
		client.loop_start()
		(rc, mid) = client.publish(topic, payload="test", qos=0)
		time.sleep(TIMEOUT)
		client.loop_stop()
		client.disconnect()
		if should_succeed:
			return userdata['published']
		else:
			return not userdata['published']
	except Exception as e:
		if should_succeed:
			print(f"[FAIL] Exception for topic {topic}: {e}")
			traceback.print_exc()
			return False
		else:
			return True  # Exception is expected for raw/*

def main():
	print("[AT-1] Testing MQTT ingress policy...")
	# Test raw/* (should be rejected)
	raw_rejected = not test_topic("raw/test", should_succeed=True)
	print(f"raw/* publish {'FAIL' if raw_rejected else 'PASS'} (should be rejected)")
	# Test sym/* (should be accepted)
	sym_accepted = test_topic("sym/test", should_succeed=True)
	print(f"sym/* publish {'PASS' if sym_accepted else 'FAIL'} (should be accepted)")
	if raw_rejected and sym_accepted:
		print("[PASS] AT-1: Symbols-Only Ingress")
		sys.exit(0)
	else:
		print("[FAIL] AT-1: Symbols-Only Ingress")
		sys.exit(1)

if __name__ == "__main__":
	main()
