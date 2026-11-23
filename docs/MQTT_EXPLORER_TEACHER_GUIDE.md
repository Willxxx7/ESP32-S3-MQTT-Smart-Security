# Teacher guide: MQTT Explorer practical

## Suggested delivery

Duration: 2 hours (or split into two lessons). Students work in pairs. Prefer a local simulator for the first lesson and physical ESP32-S3 for the second.

**Before class:** verify Mosquitto, Python 3.10+, `paho-mqtt` 2.x, MQTT Explorer and firewall settings. Confirm local-only simulation works first. For a shared lab, allocate each pair a **separate broker** or a unique topic namespace; the supplied project uses a single fixed namespace and is not multi-group isolated by default.

## Demonstration sequence

1. Sketch publisher → broker → subscriber.
2. Start Mosquitto, simulator, dashboard and MQTT Explorer.
3. Inspect telemetry and show JSON Boolean versus string.
4. Publish LED ON/OFF from Explorer and observe simulator.
5. Arm dashboard; wait for simulated motion; explain automatic buzzer response.
6. Compare QoS 0/1 without promising exactly-once behaviour.
7. Publish retained test value to `lab/security/esp32s3/lab-retained`; reconnect; clear retained test value with empty retained publish.
8. Stop local broker; demonstrate connection error and recovery.
9. Show anonymous command acceptance on a teacher-controlled isolated broker.
10. Discuss accounts, ACLs, TLS and safe device behaviour.

## Expected observations

- `telemetry` updates roughly once a second.
- `status` shows online while connected and may show offline after unexpected disconnection via the Last Will.
- Valid JSON Boolean commands change LED/buzzer state.
- The string `"true"` should not be treated as Boolean `true`.
- A retained test payload is replayed to a new subscriber.
- QoS 1 can duplicate messages; QoS 0 has no delivery acknowledgement guarantee.
- Anonymous clients can publish commands on the demo broker.

## Important implementation limitations

The simulator generates a motion event at the start of each 20-second cycle; the dashboard automation triggers on a false→true motion transition while armed. Arming is dashboard-local and does not persist. The simulator's `motion` is synthetic, while the hardware's GPIO5 button stands in for a PIR sensor. Both publish to the same topics, so run only one at a time.

The broker demo is plaintext and anonymous. Do not connect it to a public network. The secure ACL configuration in `docs/MQTT_SECURITY.md` is conceptual and requires changes to the Python and ESP32 clients to support credentials.

## Assessment prompts

Explain why a topic wildcard `#` is useful but potentially overbroad. Contrast telemetry, commands and retained status. Evaluate fault tolerance and explain how authentication, authorisation and encryption solve different security problems.

## Suggested marking

- Pass: connect, inspect topics, publish a valid command and explain publisher/broker/subscriber.
- Merit: test invalid data, QoS/retain behaviour and diagnose a fault with evidence.
- Distinction: evaluate security, failure modes and propose a defensible multi-device design with justified controls.

Adapt to the specific qualification's published assessment criteria; these are teaching indicators, not official grading rules.
