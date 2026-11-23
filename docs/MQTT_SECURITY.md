# MQTT security lab — isolated demonstration only

The starter broker configuration intentionally uses `allow_anonymous true` to make the security weakness observable. This is **not safe** on an untrusted network. Use a dedicated isolated classroom LAN or localhost; do not expose TCP 1883 to the internet or a shared institutional network.

## Demonstration: unauthorised command

1. Start the simulator and dashboard on a teacher-controlled broker.
2. Open MQTT Explorer as a second client with a unique client ID.
3. Subscribe to `lab/security/esp32s3/#`.
4. Publish `{"action":"led","value":true}` to `lab/security/esp32s3/command` with Retain OFF.
5. Observe that the simulator accepts the command without knowing who sent it.
6. Explain the difference between an MQTT topic, client ID and verified identity. A client ID alone is **not** authentication.

Use the simulator for the demonstration if physical actuators could create a hazard.

## Harden the broker (illustrative Mosquitto setup)

On a trusted lab PC, create a Mosquitto password file with `mosquitto_passwd -c passwords.txt teacher`, then add a second account with `mosquitto_passwd passwords.txt observer`. Do not commit this password file.

Create an ACL file `acl.txt` containing:

```text
user teacher
topic readwrite lab/security/esp32s3/#

user observer
topic read lab/security/esp32s3/telemetry
topic read lab/security/esp32s3/status
topic read lab/security/esp32s3/event
```

A broker configuration can then use:

```text
listener 1883 127.0.0.1
allow_anonymous false
password_file /ABSOLUTE/PATH/TO/passwords.txt
acl_file /ABSOLUTE/PATH/TO/acl.txt
```

Use a real absolute file path appropriate to your system and test Mosquitto's file access. This example binds to localhost only. For an ESP32 on a private LAN, change the listener address deliberately and add a dedicated device account with minimum required topic permissions. The current Python and MicroPython code do **not** accept MQTT usernames/passwords; they must be extended before using this authenticated broker. The example above is a teacher-led hardening exercise, not a drop-in replacement for the starter configuration.

## Additional controls

- Use TLS and certificate validation on untrusted networks; credentials sent over plaintext MQTT can be intercepted.
- Give each client a unique ID and individual credentials.
- Use per-device topics to avoid one device controlling another.
- Apply least-privilege ACLs: observers read telemetry; controllers publish commands; devices publish telemetry and subscribe to their own commands.
- Never retain actuator commands unless the device explicitly implements safe state reconciliation.
- Validate JSON schemas and payload size; avoid trusting message origin without authentication.
- Define a safe disconnected state for actuators, and audit sensitive commands.

## Discussion prompts

How would you detect an unauthorised publisher? What evidence would you log? Why do ACLs provide a stronger control than obscuring a topic name? How does MQTT over WebSockets differ from MQTT over TCP, and why does WebSockets alone not imply encryption?
