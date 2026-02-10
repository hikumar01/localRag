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

import argparse
from typing import List, Optional

def main(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(prog="python -m src.cli")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ingest = sub.add_parser("ingest")
    p_ingest.add_argument("--skip-ocr", action="store_true")
    p_ingest.add_argument("--skip-video", action="store_true")
    p_ingest.add_argument("--workers", type=int, default=None)

    sub.add_parser("cluster")
    sub.add_parser("summarize")
    sub.add_parser("confidence")
    sub.add_parser("timeline")
    sub.add_parser("deps")
    sub.add_parser("mermaid")
    sub.add_parser("roadmap")
    sub.add_parser("risks")
    sub.add_parser("rag")

    args = parser.parse_args(argv)

    if args.cmd == "ingest":
        ingest(skip_ocr=args.skip_ocr, skip_video=args.skip_video, workers=args.workers)
    elif args.cmd == "cluster":
        cluster()
    elif args.cmd == "summarize":
        summarize()
    elif args.cmd == "confidence":
        confidence()
    elif args.cmd == "timeline":
        timeline()
    elif args.cmd == "deps":
        deps()
    elif args.cmd == "mermaid":
        mermaid()
    elif args.cmd == "roadmap":
        roadmap()
    elif args.cmd == "risks":
        risks()
    elif args.cmd == "rag":
        index()

if __name__ == "__main__":
    main()
