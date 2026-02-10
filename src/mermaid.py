import networkx as nx
from pathlib import Path
import json

def run():
    for p in Path("data/projects").iterdir():
        gpath = p / "dependencies.graphml"
        if not gpath.exists():
            continue

        g = nx.read_graphml(gpath)
        lines = ["graph TD"]
        for u, v in g.edges():
            lines.append(f"  {u} --> {v}")
        (p / "dependencies.mmd").write_text("\n".join(lines))
