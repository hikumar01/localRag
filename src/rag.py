import ollama, chromadb
from chromadb.config import Settings
from typing import Optional
from pathlib import Path

# Persistent Chroma DB
client = chromadb.Client(
    Settings(
        persist_directory="data/chroma",
        anonymized_telemetry=False
    )
)

# -----------------------
# Indexing
# -----------------------

def index():
    for p in Path("data/projects").iterdir():
        col = client.get_or_create_collection(p.name)

        text = (p / "summary.md").read_text()

        col.add(
            documents=[text],
            ids=[f"{p.name}_summary"]
        )

# -----------------------
# RAG
# -----------------------

# def ask(question: str, project_id: str | None = None) -> str:
def ask(question: str, project_id: Optional[str] = None) -> str:
    if project_id:
        col = client.get_or_create_collection(project_id)

        res = col.query(
            query_texts=[question],
            n_results=3
        )

        docs = res["documents"][0] if res["documents"] else []
    else:
        # Global search across all collections
        docs = []

        for col_meta in client.list_collections():
            col = client.get_collection(col_meta.name)
            res = col.query(query_texts=[question], n_results=1)

            if res["documents"]:
                docs.extend(res["documents"][0])

    context = "\n---\n".join(docs) if docs else "No relevant context found."

    prompt = f"""
You are an expert project analyst.

Use the context below to answer the question.

Context:
{context}

Question:
{question}

Answer clearly and concisely in markdown.
"""

    out = ollama.generate(
        model="llama3:8b",
        prompt=prompt
    )

    return out["response"]
