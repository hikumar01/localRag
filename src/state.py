import json, hashlib
from pathlib import Path

STATE = Path("data/cache/state.json")

def load_state():
    if not STATE.exists():
        return {}

    try:
        text = STATE.read_text().strip()
        return json.loads(text) if text else {}
    except json.JSONDecodeError:
        # Corrupt or partial state file → reset safely
        return {}

def save_state(state):
    STATE.parent.mkdir(parents=True, exist_ok=True)

    # atomic write: write temp → rename
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2))
    tmp.replace(STATE)

def file_hash(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
