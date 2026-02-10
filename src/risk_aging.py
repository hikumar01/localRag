import json
from pathlib import Path
from datetime import datetime

def run():
    for p in Path("data/projects").iterdir():
        risks = []
        text = (p / "summary.md").read_text()
        if "risk" in text.lower():
            risks.append({
                "text": "Identified risk",
                "first_seen": datetime.now().isoformat()
            })
        (p / "risk_aging.json").write_text(
            json.dumps(risks, indent=2)
        )
