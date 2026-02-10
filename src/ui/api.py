from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json
import markdown

from ..rag import ask

BASE_DIR = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = BASE_DIR / "src/ui/templates"
PROJECTS_DIR = BASE_DIR / "data/projects"

assert TEMPLATES_DIR.exists(), f"Templates missing: {TEMPLATES_DIR}"

app = FastAPI(title="Project Intel")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def read_json(p: Path, default):
    return json.loads(p.read_text()) if p.exists() else default


@app.get("/", response_class=HTMLResponse)
def home(req: Request):
    projects = sorted(
        [p.name for p in PROJECTS_DIR.iterdir() if p.is_dir()]
    ) if PROJECTS_DIR.exists() else []

    return templates.TemplateResponse(
        "index.html",
        {"request": req, "projects": projects}
    )


@app.get("/project/{pid}", response_class=HTMLResponse)
def project(pid: str, req: Request):
    p = PROJECTS_DIR / pid

    summary_md = (p / "summary.md").read_text() if (p / "summary.md").exists() else ""
    summary_html = markdown.markdown(summary_md, extensions=["tables", "fenced_code"])

    return templates.TemplateResponse(
        "project.html",
        {
            "request": req,
            "pid": pid,
            "summary": summary_html,
            "confidence": read_json(p / "confidence.json", {}),
            "timeline": read_json(p / "timeline.json", []),
            "risks": read_json(p / "risks.json", []),
            "roadmap": read_json(p / "roadmap.json", []),
            "deps": read_json(p / "dependencies.json", {}),
        }
    )


@app.post("/rag/{pid}", response_class=HTMLResponse)
def rag_project(pid: str, req: Request, q: str = Form(...)):
    answer_md = ask(question=q, project_id=pid)
    answer_html = markdown.markdown(
        answer_md,
        extensions=["tables", "fenced_code"]
    )

    return templates.TemplateResponse(
        "rag.html",
        {
            "request": req,
            "pid": pid,
            "question": q,
            "answer": answer_html
        }
    )


@app.post("/rag", response_class=HTMLResponse)
def rag_global(req: Request, q: str = Form(...)):
    answer_md = ask(question=q)
    answer_html = markdown.markdown(
        answer_md,
        extensions=["tables", "fenced_code"]
    )

    return templates.TemplateResponse(
        "rag.html",
        {
            "request": req,
            "pid": None,
            "question": q,
            "answer": answer_html
        }
    )


@app.get("/compare", response_class=HTMLResponse)
def compare(req: Request, a: str, b: str):
    pa, pb = PROJECTS_DIR / a, PROJECTS_DIR / b

    return templates.TemplateResponse(
        "compare.html",
        {
            "request": req,
            "a": a,
            "b": b,
            "ca": read_json(pa / "confidence.json", {}),
            "cb": read_json(pb / "confidence.json", {}),
            "ra": read_json(pa / "risks.json", []),
            "rb": read_json(pb / "risks.json", []),
        }
    )
