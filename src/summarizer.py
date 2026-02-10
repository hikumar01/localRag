import ollama, yaml, json
from pathlib import Path

PROJECTS = Path("data/projects")
TEMPLATE = yaml.safe_load(
    Path("config/pm_template.yaml").read_text()
)

def run():
    for p in PROJECTS.iterdir():
        files = json.loads((p / "files.json").read_text())
        content = ""

        for f in files:
            content += Path(f).read_text() + "\n"

        prompt = f"""
You are a Technical Product Manager.
Create an onboarding summary.

Template:
{TEMPLATE}

Content:
{content[:8000]}
"""

        res = ollama.generate(
            model="llama3:8b", prompt=prompt
        )["response"]

        (p / "summary.md").write_text(res)
