import ollama, json
from pathlib import Path
from sklearn.cluster import AgglomerativeClustering

EXTRACTED = Path("data/extracted")
PROJECTS = Path("data/projects")

def run():
    texts, paths = [], []

    for f in EXTRACTED.rglob("*.txt"):
        t = f.read_text().strip()
        if t:
            texts.append(t[:1000])
            paths.append(str(f))

    embeds = [
        ollama.embeddings(
            model="nomic-embed-text", prompt=t
        )["embedding"]
        for t in texts
    ]

    labels = AgglomerativeClustering(
        n_clusters=None, distance_threshold=1.1
    ).fit_predict(embeds)

    clusters = {}
    for l, p in zip(labels, paths):
        clusters.setdefault(str(l), []).append(p)

    for cid, files in clusters.items():
        pdir = PROJECTS / f"project_{cid}"
        pdir.mkdir(parents=True, exist_ok=True)
        (pdir / "files.json").write_text(
            json.dumps(files, indent=2)
        )
