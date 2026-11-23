import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'desktop'))
from common import parse_message

def test_json_object():
    assert parse_message(b'{"led":true}') == {'led': True}

def test_reject_array():
    try:
        parse_message(b'[]')
    except ValueError:
        return
    assert False, 'Expected ValueError'
