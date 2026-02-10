from .ingest import run as ingest
from .clustering import run as cluster
from .summarizer import run as summarize
from .confidence import run as confidence
from .timeline import run as timeline
from .dependency_graph import run as deps
from .mermaid import run as mermaid
from .roadmap import run as roadmap
from .risk_aging import run as risks
from .rag import index

import sys

cmd = sys.argv[1]

if cmd == "ingest": ingest()
elif cmd == "cluster": cluster()
elif cmd == "summarize": summarize()
elif cmd == "confidence": confidence()
elif cmd == "timeline": timeline()
elif cmd == "deps": deps()
elif cmd == "mermaid": mermaid()
elif cmd == "roadmap": roadmap()
elif cmd == "risks": risks()
elif cmd == "rag": index()
