# MQTT Explorer investigation — learner worksheet

**Project:** ESP32-S3 Smart Security Lab  
**Suggested duration:** 90–120 minutes plus extension  
**Prerequisites:** Python simulator or connected ESP32-S3, Mosquitto, MQTT Explorer

## Learning outcomes

By the end you should be able to explain the MQTT broker/publisher/subscriber model; inspect topics and JSON; test QoS and retained messages; diagnose faults; and explain why an unauthenticated command topic is insecure.

## Task 1 — Trace the architecture (15 minutes)

1. Draw the path of a telemetry message from the ESP32/simulator to MQTT Explorer.
2. Identify which components are publishers, subscribers and the broker.
3. Explain why MQTT Explorer does not normally connect directly to the ESP32.
4. Connect to the broker using `docs/MQTT_EXPLORER_SETUP.md`. Record the host, port, client ID and subscription filter.

**Evidence:** architecture diagram and connection screenshot.

## Task 2 — Subscribe and inspect JSON (15 minutes)

Subscribe to `lab/security/esp32s3/#`. Identify the `telemetry`, `event`, `status` and `command` topics.

Record two telemetry payloads. Explain the meaning and data type of `motion`, `led`, `buzzer` and `uptime_s`. Explain the difference between a topic and its payload.

**Evidence:** topic-tree screenshot and annotated JSON.

## Task 3 — Publish commands (15 minutes)

Publish these **non-retained** JSON messages to `lab/security/esp32s3/command`:

- `{"action":"led","value":true}`
- `{"action":"led","value":false}`
- `{"action":"buzzer","value":true}`
- `{"action":"buzzer","value":false}`

Record the effect in the simulator terminal or on the actual hardware. Predict the outcome of `{"action":"led","value":"true"}` (string instead of Boolean), then test it. Explain why type validation matters.

**Evidence:** four command results and one invalid-type test.

## Task 4 — QoS investigation (15 minutes)

Using MQTT Explorer, publish a test event to `lab/security/esp32s3/event` at QoS 0 and then QoS 1, where the client allows selecting QoS. Describe the delivery guarantees of QoS 0 (at most once) and QoS 1 (at least once, so duplicates are possible). If the broker or client limits QoS selection, explain that limitation.

Do **not** claim a single successful delivery proves a QoS guarantee. Design a repeatable experiment involving network interruption and message counts, and state its limitations.

**Evidence:** QoS settings, observations and evaluation.

## Task 5 — Retained messages (15 minutes)

Publish `{"state":"lesson-demo"}` to `lab/security/esp32s3/lab-retained` with **Retain ON**. Disconnect and reconnect MQTT Explorer, then subscribe to that topic. Explain why the last retained value appears for a new subscriber.

Clear the retained message by publishing an **empty payload** with Retain ON to the same test topic. Do not retain commands to the real actuator topic: a reconnecting device could unexpectedly repeat an old command.

**Evidence:** before/after screenshots and explanation.

## Task 6 — Fault finding (15 minutes)

With the teacher's permission, stop the **local test broker** or disconnect your own test client. Record the error and investigate whether the cause is the broker, wrong IP, blocked port, subscription mismatch or duplicate client ID. Restore service and verify that new telemetry appears.

**Evidence:** diagnostic checklist and successful recovery.

## Task 7 — Security challenge (20 minutes)

On the teacher's **isolated lab broker only**, publish a benign LED command from a second MQTT Explorer client. Observe whether it is accepted without authentication.

Answer:
1. What does this demonstrate about anonymous publishing?
2. What is the difference between authentication and authorisation?
3. How could a topic ACL restrict one client to reading telemetry but not publishing commands?
4. Why would TLS matter on an untrusted network?
5. What should the ESP32 do if the broker connection is lost?

**Evidence:** observed result and a proposed secure design. Do not test against other students' devices, external brokers or institutional systems without permission.

## Extension / distinction

Design a topic namespace for **three** ESP32 devices with unique IDs. Propose per-device command ACLs, QoS selection, retained state rules and an SQLite event audit trail. Evaluate reliability, latency, bandwidth, privacy and safe failure.

## Assessment checklist

- [ ] Correct broker/client architecture
- [ ] Successful topic subscription and JSON interpretation
- [ ] Valid and invalid command tests
- [ ] Accurate QoS 0/1 comparison
- [ ] Retained-message test and cleanup
- [ ] Fault diagnosis with evidence
- [ ] Security risks and justified mitigations
- [ ] Evaluation supported by screenshots and observations
