# ESP32-S3 MQTT Smart Security Lab

A Python and MicroPython classroom starter: ESP32-S3 MQTT node, Tkinter dashboard, Mosquitto broker and hardware-free simulator.

## Network
Windows runs Mosquitto and the dashboard. The ESP32-S3 and PC need a reachable local Wi-Fi network (for example a compatible phone hotspot). College Wi-Fi may block device-to-device connections. An unidentified USB dongle is not assumed compatible. The ESP32-S3 has built-in 2.4 GHz Wi-Fi.

## Windows setup
Install Python 3.10+ and Eclipse Mosquitto. In VS Code:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

For local simulation, run Mosquitto with a localhost listener (default local-only Mosquitto configuration may work). In separate terminals:

```powershell
.\.venv\Scripts\python.exe desktop/simulator.py --broker 127.0.0.1
.\.venv\Scripts\python.exe desktop/dashboard.py --broker 127.0.0.1
```

For a real ESP32, edit `broker/mosquitto.conf` and replace `YOUR_PC_LAN_IP` with the Windows IPv4 address from `ipconfig`, then run `mosquitto -c broker/mosquitto.conf -v`. Allow TCP 1883 through the Windows firewall on a **trusted private network only**. This sample broker permits anonymous, unencrypted MQTT and must not be exposed to public or college networks.

## ESP32-S3 setup
Flash an ESP32-S3-specific MicroPython firmware build using Thonny or esptool. Copy `esp32/config_example.py` to `esp32/config.py`, enter your 2.4 GHz Wi-Fi credentials and PC broker IPv4 address, and upload `config.py` and `main.py` to the board. The firmware needs `umqtt.simple` installed if not included in the build. **Never commit `config.py` or real credentials.**

### Example wiring — verify board pinout first
- GPIO4 → 220–330 Ω resistor → LED anode; LED cathode → GND.
- GPIO5 → push button → GND (internal pull-up).
- GPIO6 → compatible low-current 3.3 V active buzzer → GND; use a driver for higher-current devices.
- The button simulates motion detection until a suitable PIR sensor is added.

## MQTT topics
- `lab/security/esp32s3/telemetry`: JSON state and uptime.
- `lab/security/esp32s3/event`: motion event.
- `lab/security/esp32s3/command`: LED/buzzer JSON commands.
- `lab/security/esp32s3/status`: retained online/offline state.

The dashboard provides arm/disarm controls and a basic rule that activates the buzzer when motion is detected while armed. Arming is dashboard-local, not persistent. The simulator and real board share MQTT topics: **do not run both simultaneously**. This is a teaching prototype, not a certified security system.

## Learning activities
See [docs/LESSON.md](docs/LESSON.md) for MQTT, validation, QoS, cybersecurity and hardware extensions.

## Future enhancements
PIR sensor, environmental telemetry, SQLite event log, access control, authenticated MQTT, TLS, reconnect tests and a richer dashboard.

## MQTT Explorer practical

MQTT Explorer is a separate desktop client for inspecting MQTT topics and publishing test messages. Start with [MQTT Explorer setup](docs/MQTT_EXPLORER_SETUP.md), then use the [learner worksheet](docs/MQTT_EXPLORER_LEARNER_WORKSHEET.md), [teacher guide](docs/MQTT_EXPLORER_TEACHER_GUIDE.md), [security lab](docs/MQTT_SECURITY.md) and [sample payloads](examples/mqtt_messages.jsonl).

For a local-only test, connect MQTT Explorer to `127.0.0.1:1883` and subscribe to `lab/security/esp32s3/#`. Never retain actuator commands. The anonymous broker is for isolated demonstration only.
