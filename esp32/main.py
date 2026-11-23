"""ESP32-S3 MicroPython MQTT security node (umqtt.simple firmware module needed)."""
import time
import json
import network
from machine import Pin
from umqtt.simple import MQTTClient
import config

BASE = 'lab/security/esp32s3'
TELEMETRY = (BASE + '/telemetry').encode()
EVENT = (BASE + '/event').encode()
COMMAND = (BASE + '/command').encode()
STATUS = (BASE + '/status').encode()

LED = Pin(4, Pin.OUT, value=0)
BUTTON = Pin(5, Pin.IN, Pin.PULL_UP)
BUZZER = Pin(6, Pin.OUT, value=0)
state = {'led': False, 'buzzer': False, 'motion': False}

def publish_json(client, topic, obj, retain=False):
    client.publish(topic, json.dumps(obj).encode(), retain=retain)

def on_command(topic, payload):
    try:
        cmd = json.loads(payload.decode())
        if not isinstance(cmd, dict):
            return
        action, value = cmd.get('action'), cmd.get('value')
        if action in ('led', 'buzzer') and type(value) is bool:
            state[action] = value
            (LED if action == 'led' else BUZZER).value(int(value))
    except (ValueError, TypeError) as exc:
        print('Bad command:', exc)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
    for _ in range(30):
        if wlan.isconnected():
            print('Wi-Fi IP:', wlan.ifconfig()[0])
            return
        time.sleep(1)
    raise OSError('Wi-Fi connection timeout')

def run():
    connect_wifi()
    client = MQTTClient(config.CLIENT_ID, config.BROKER_IP, port=config.BROKER_PORT, keepalive=30)
    client.set_callback(on_command)
    client.set_last_will(STATUS, b'{"state":"offline"}', retain=True)
    client.connect()
    client.subscribe(COMMAND)
    publish_json(client, STATUS, {'state': 'online', 'mode': 'hardware'}, retain=True)
    start = time.ticks_ms()
    last_motion = False
    last_publish = time.ticks_ms()
    try:
        while True:
            client.check_msg()
            motion = BUTTON.value() == 0
            state['motion'] = motion
            if motion and not last_motion:
                publish_json(client, EVENT, {'event': 'motion_detected', 'source': 'button'})
            last_motion = motion
            if time.ticks_diff(time.ticks_ms(), last_publish) >= 1000:
                publish_json(client, TELEMETRY, dict(state, uptime_s=time.ticks_diff(time.ticks_ms(), start) // 1000))
                last_publish = time.ticks_ms()
            time.sleep_ms(50)
    finally:
        LED.off()
        BUZZER.off()
        client.disconnect()

while True:
    try:
        run()
    except Exception as exc:
        print('Disconnected; retrying in 5 seconds:', exc)
        LED.off()
        BUZZER.off()
        time.sleep(5)
