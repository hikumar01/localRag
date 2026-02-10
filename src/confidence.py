import json
from pathlib import Path

def run():
    for p in Path("data/projects").iterdir():
        summary = (p / "summary.md").read_text()
        score = round(min(len(summary) / 6000, 1.0), 2)
        (p / "confidence.json").write_text(
            json.dumps({"overall": score}, indent=2)
        )
