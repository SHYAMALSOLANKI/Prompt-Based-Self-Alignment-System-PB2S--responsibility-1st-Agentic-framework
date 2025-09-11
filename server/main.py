import time, json, threading
from collections import deque
import paho.mqtt.client as mq

BROKER="localhost"; QOS=1
BUF = deque(maxlen=64)
state = {"mode":"FAIR","risk": {"audio":0.0,"vision":0.0}}

def novelty(e): return e.get("novelty",0.0)
def policy_priority(e): return e.get("priority",0.0)

def on_msg(_c,_u,msg):
    try: BUF.append(json.loads(msg.payload))
    except: pass

def select_focus():
    best,score=None,-1e9
    for e in list(BUF):
        s=0.4*novelty(e)+0.3*state["risk"].get(e.get("source",""),0.0)+0.2*policy_priority(e)-0.1*e.get("age",0.0)
        if s>score: best,score=e,s
    return best

def tick(client):
    while True:
        f = select_focus()
        if f:
            req = {"v":1,"context":f,"facts":[],"policy":{"maxCycles":2,"temp":0.2}}
            client.publish("planner/requests", json.dumps(req), qos=QOS)
        time.sleep(0.1)  # 10Hz scan

def main():
    c = mq.Client(client_id="attention")
    c.on_message=on_msg
    c.connect(BROKER,1883,60)
    c.subscribe("sym/#", qos=0)
    threading.Thread(target=tick, args=(c,), daemon=True).start()
    c.loop_forever()

if __name__ == "__main__":
    main()
