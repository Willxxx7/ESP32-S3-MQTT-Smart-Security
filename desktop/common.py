import json
BASE = 'lab/security/esp32s3'
TELEMETRY = BASE + '/telemetry'
EVENT = BASE + '/event'
COMMAND = BASE + '/command'
STATUS = BASE + '/status'

def parse_message(payload):
    obj = json.loads(payload.decode('utf-8'))
    if not isinstance(obj, dict):
        raise ValueError('Expected JSON object')
    return obj
