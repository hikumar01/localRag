import json
from pathlib import Path

def compare(a, b):
    pa = Path("data/projects") / a
    pb = Path("data/projects") / b

    return {
        a: json.loads((pa / "confidence.json").read_text()),
        b: json.loads((pb / "confidence.json").read_text())
    }
