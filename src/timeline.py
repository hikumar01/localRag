import json
from pathlib import Path
from datetime import datetime

def run():
    for p in Path("data/projects").iterdir():
        events = []
        for line in (p / "summary.md").read_text().splitlines():
            if "decide" in line.lower():
                events.append({
                    "date": datetime.now().isoformat(),
                    "event": line
                })
        (p / "timeline.json").write_text(
            json.dumps(events, indent=2)
        )
