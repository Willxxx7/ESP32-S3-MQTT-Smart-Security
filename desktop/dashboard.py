"""Tkinter MQTT dashboard. Requires Mosquitto and paho-mqtt 2.x."""
import argparse
import json
import queue
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import paho.mqtt.client as mqtt
from common import COMMAND, EVENT, STATUS, TELEMETRY, parse_message

parser = argparse.ArgumentParser()
parser.add_argument('--broker', default='127.0.0.1')
parser.add_argument('--port', type=int, default=1883)
args = parser.parse_args()

messages = queue.Queue()
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id='security-dashboard')

def on_connect(c, userdata, flags, reason_code, properties):
    messages.put(('system', 'Broker connection: ' + str(reason_code)))
    if reason_code == 0:
        c.subscribe([(TELEMETRY, 0), (EVENT, 0), (STATUS, 0)])

def on_disconnect(c, userdata, disconnect_flags, reason_code, properties):
    messages.put(('system', 'Disconnected: ' + str(reason_code)))

def on_message(c, userdata, msg):
    try:
        messages.put((msg.topic, parse_message(msg.payload)))
    except (ValueError, UnicodeError) as exc:
        messages.put(('system', 'Invalid message: ' + str(exc)))

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect_async(args.broker, args.port, keepalive=30)
client.loop_start()

root = tk.Tk()
root.title('ESP32-S3 MQTT Security Dashboard')
root.geometry('740x520')
armed = False
status_var = tk.StringVar(value='Connecting...')
telemetry_var = tk.StringVar(value='Waiting for telemetry')

header = ttk.Frame(root, padding=12)
header.pack(fill='x')
ttk.Label(header, text='SMART SECURITY CONTROL CENTRE', font=('Segoe UI', 16, 'bold')).pack(anchor='w')
ttk.Label(header, textvariable=status_var).pack(anchor='w')
ttk.Label(header, textvariable=telemetry_var).pack(anchor='w')
controls = ttk.Frame(root, padding=12)
controls.pack(fill='x')
log = tk.Text(root, height=20, state='disabled')
log.pack(fill='both', expand=True, padx=12, pady=12)

def append(text):
    log.configure(state='normal')
    log.insert('end', f'{datetime.now():%H:%M:%S}  {text}\n')
    log.see('end')
    log.configure(state='disabled')

def command(action, value):
    payload = json.dumps({'action': action, 'value': value})
    result = client.publish(COMMAND, payload, qos=0, retain=False)
    append(f'Command: {payload} (publish rc={result.rc})')

def set_arm(value):
    global armed
    armed = value
    append('System ' + ('ARMED' if armed else 'DISARMED'))

ttk.Button(controls, text='Arm', command=lambda: set_arm(True)).pack(side='left', padx=4)
ttk.Button(controls, text='Disarm', command=lambda: set_arm(False)).pack(side='left', padx=4)
for label, action, value in [('LED ON', 'led', True), ('LED OFF', 'led', False),
                             ('Buzzer ON', 'buzzer', True), ('Buzzer OFF', 'buzzer', False)]:
    ttk.Button(controls, text=label, command=lambda a=action, v=value: command(a, v)).pack(side='left', padx=4)

last_motion = False

def poll():
    global last_motion
    try:
        while True:
            topic, data = messages.get_nowait()
            if topic == TELEMETRY:
                telemetry_var.set('Telemetry: ' + str(data))
                motion = data.get('motion') is True
                if armed and motion and not last_motion:
                    append('ALERT: Motion detected while armed!')
                    command('buzzer', True)
                last_motion = motion
            elif topic == STATUS:
                status_var.set('Device status: ' + str(data))
            else:
                append(f'{topic}: {data}')
    except queue.Empty:
        pass
    root.after(100, poll)

def shutdown():
    client.disconnect()
    client.loop_stop()
    root.destroy()

root.protocol('WM_DELETE_WINDOW', shutdown)
root.after(100, poll)
root.mainloop()
