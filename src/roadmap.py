import json
from pathlib import Path

def run():
    for p in Path("data/projects").iterdir():
        timeline = json.loads((p / "timeline.json").read_text())
        roadmap = {"Discovery": [], "Build": [], "Launch": []}

        for e in timeline:
            t = e["event"].lower()
            if "decide" in t:
                roadmap["Discovery"].append(e)
            elif "build" in t:
                roadmap["Build"].append(e)
            else:
                roadmap["Launch"].append(e)

        (p / "roadmap.json").write_text(
            json.dumps(roadmap, indent=2)
        )
