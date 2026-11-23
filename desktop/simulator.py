"""Simulated ESP32-S3: runs without hardware."""
import argparse
import json
import time
import paho.mqtt.client as mqtt
from common import COMMAND, EVENT, STATUS, TELEMETRY, parse_message

parser = argparse.ArgumentParser()
parser.add_argument('--broker', default='127.0.0.1')
parser.add_argument('--port', type=int, default=1883)
args = parser.parse_args()
state = {'led': False, 'buzzer': False, 'motion': False}
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id='esp32s3-simulator')
client.will_set(STATUS, json.dumps({'state': 'offline'}), qos=0, retain=True)

def on_connect(c, userdata, flags, reason_code, properties):
    if reason_code == 0:
        c.subscribe(COMMAND)
        c.publish(STATUS, json.dumps({'state': 'online', 'mode': 'simulation'}), retain=True)

def on_message(c, userdata, msg):
    try:
        obj = parse_message(msg.payload)
        action, value = obj.get('action'), obj.get('value')
        if action in ('led', 'buzzer') and type(value) is bool:
            state[action] = value
            print('Updated:', action, value)
    except (ValueError, UnicodeError) as exc:
        print('Rejected command:', exc)

client.on_connect = on_connect
client.on_message = on_message
client.connect(args.broker, args.port, 30)
client.loop_start()
start = time.monotonic()
try:
    while True:
        elapsed = int(time.monotonic() - start)
        state['motion'] = elapsed % 20 < 5
        payload = {**state, 'uptime_s': elapsed}
        client.publish(TELEMETRY, json.dumps(payload))
        if elapsed % 20 == 0:
            client.publish(EVENT, json.dumps({'event': 'motion_detected', 'simulated': True}))
        time.sleep(1)
except KeyboardInterrupt:
    client.publish(STATUS, json.dumps({'state': 'offline'}), retain=True)
    client.disconnect()
    client.loop_stop()
