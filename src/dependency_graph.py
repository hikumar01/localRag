import networkx as nx
from pathlib import Path

def run():
    for p in Path("data/projects").iterdir():
        g = nx.DiGraph()
        text = (p / "summary.md").read_text()
        if "api" in text.lower():
            g.add_edge("Frontend", "Backend")
        nx.write_graphml(g, p / "dependencies.graphml")
