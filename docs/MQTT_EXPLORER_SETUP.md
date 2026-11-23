# MQTT Explorer: setup and first connection

MQTT Explorer is a desktop MQTT client (not the Mosquitto broker). It connects to Mosquitto alongside the Python dashboard and ESP32-S3.

## Lab topology

- Windows PC: Mosquitto broker and Python dashboard.
- MQTT Explorer: on the same PC or another permitted device.
- ESP32-S3: MicroPython client using built-in 2.4 GHz Wi-Fi.
- The simulator can stand in for the ESP32-S3 when hardware is unavailable.

Do not run the simulator and real board simultaneously: they use the same device topics and their status/telemetry will conflict.

## A. Local simulation (no ESP32, no network)

1. Install Mosquitto and MQTT Explorer. Use a Mosquitto instance listening on `127.0.0.1:1883`; the supplied network configuration is **not** needed for this local-only exercise.
2. In one terminal run the broker, for example `mosquitto -p 1883 -v`. Stop any existing Mosquitto service first if port 1883 is already occupied.
3. In VS Code, install dependencies: `py -m pip install -r requirements.txt`.
4. Run `py desktop/simulator.py --broker 127.0.0.1` and `py desktop/dashboard.py --broker 127.0.0.1` in separate terminals.
5. Open MQTT Explorer, add a connection with Host `127.0.0.1`, Port `1883`, MQTT (not WebSockets), and a unique client ID such as `student-explorer-01`.
6. Connect and subscribe to `lab/security/esp32s3/#` if MQTT Explorer prompts for a subscription. Observe the topic tree and payloads.
7. Publish to `lab/security/esp32s3/command` with payload `{"action":"led","value":true}` and **Retain OFF**. Observe the simulator terminal and dashboard.

## B. Real ESP32-S3 (private LAN only)

1. Connect the PC and ESP32 to the same **reachable** private Wi-Fi network. A phone hotspot may isolate clients, and a college network may restrict this traffic.
2. Find the PC's LAN IPv4 address using `ipconfig`. Do **not** use `127.0.0.1` on the ESP32: it points back to the ESP32.
3. Edit `broker/mosquitto.conf` to replace `YOUR_PC_LAN_IP` with the PC IPv4 address; start Mosquitto with `mosquitto -c broker/mosquitto.conf -v`. Allow TCP 1883 through the Windows firewall for the chosen trusted private network only.
4. Copy `esp32/config_example.py` to `esp32/config.py`, set Wi-Fi credentials and `BROKER_IP`, then upload `config.py` and `main.py` to the board. Install `umqtt.simple` if your MicroPython firmware lacks it.
5. In MQTT Explorer on the PC, use the PC LAN IPv4 address and port 1883; run the Python dashboard with `--broker YOUR_PC_LAN_IP`.
6. Check `lab/security/esp32s3/status` for an online message. Press the GPIO5 button to generate a motion event; publish LED commands to test GPIO4.

The example uses an anonymous plaintext MQTT broker **only for a trusted isolated teaching demonstration**. Never expose port 1883 to the internet. See `docs/MQTT_SECURITY.md` before using a shared or college network.

## Expected topics

| Topic | Publisher | Example |
| --- | --- | --- |
| `lab/security/esp32s3/telemetry` | ESP32/simulator | `{"led":false,"buzzer":false,"motion":false,"uptime_s":42}` |
| `lab/security/esp32s3/event` | ESP32/simulator | `{"event":"motion_detected"}` |
| `lab/security/esp32s3/command` | Dashboard/Explorer | `{"action":"led","value":true}` |
| `lab/security/esp32s3/status` | ESP32/simulator | `{"state":"online"}` |

The `status` topic is retained; command messages should **not** be retained. MQTT Explorer may display the latest message for a topic rather than a full durable history. To collect evidence, take timestamped screenshots and use the dashboard log.

## Troubleshooting

- Connection refused: check Mosquitto is running and listening on the intended address/port.
- Access denied: check broker username/password/ACL settings and client permissions.
- Timeout: verify IP address, firewall, network isolation and Wi-Fi connectivity.
- No topic data: verify exact topic spelling, subscription wildcard `#`, and whether the ESP32/simulator is running.
- Unexpected disconnects: use unique MQTT client IDs. Two clients sharing an ID will kick each other off.
- Device stays offline: check Wi-Fi credentials, 2.4 GHz support, MicroPython serial output, and the broker address.
- Browser-based clients generally need a separate WebSockets listener; MQTT Explorer desktop uses TCP MQTT on port 1883 in this lab.
