# Learner activities

1. Explain the publisher/broker/subscriber architecture and trace a JSON command from Tkinter to GPIO.
2. Run the simulator and record MQTT telemetry and events.
3. Test invalid JSON, wrong data types, broker disconnection and reconnection.
4. Compare MQTT QoS 0/1 and retained messages; discuss duplicates and stale commands.
5. Add a PIR sensor with appropriate voltage levels and debounce; verify pinout.
6. Extend the dashboard with SQLite event logging and charts.
7. Implement authentication and topic ACLs on Mosquitto; explain why plaintext MQTT is unsuitable on untrusted networks.
8. Evaluate privacy, bandwidth, power consumption and resilience.

## Important limitations

The starter uses a trusted private network and anonymous MQTT, not secure for public or institutional networks. Arming state is dashboard-only and is lost on restart. The button simulates a motion detector. A buzzer may need a transistor driver. The ESP32 MicroPython firmware must include `umqtt.simple` or the module must be installed on the board. A phone hotspot must permit peer-to-peer clients. A separate USB dongle attached to the ESP32 is not supported without hardware identification.
