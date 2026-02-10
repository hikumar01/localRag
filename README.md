Alright — below is a single, authoritative, copy-pasteable answer that gives you:
✅ Exact folder & file structure
✅ Complete runnable code (no pseudo, no gaps)
✅ First-time setup
✅ Daily / incremental runs
✅ MacBook Air–safe defaults
✅ Offline, read-only input
✅ All advanced PM features included:
Confidence scoring
Change safety
Mermaid graphs
Project comparison
Risk aging
Roadmap inference
RAG assistant
FastAPI UI

First-time setup (ONE TIME)
2.1 System dependencies (macOS)
brew install ollama ffmpeg tesseract libreoffice antiword pandoc poppler

2.2 Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

ollama serve

2.3 Ollama models (download once)
ollama pull llama3:8b
ollama pull nomic-embed-text

Recommended Ollama models (practical, not hype)
Model	Use	MacBook Air Friendly
llama3:8b	Main summarization	✅ Yes
mistral:7b	Faster summaries	✅ Yes
qwen2.5:7b	Structured summaries	✅ Yes
llava:7b	Image understanding	⚠️ Works but slower


3️⃣ Input folder (READ-ONLY, SYMLINK)
cd ~/project-intel/data
ln -s /absolute/path/to/your/projects input
chmod -R a-w /absolute/path/to/your/projects

7️⃣ How YOU use it
First time
python -m src.cli ingest
Optional fast first pass (no OCR/video)
python -m src.cli ingest --skip-ocr --skip-video
python -m src.cli cluster
python -m src.cli summarize
python -m src.cli confidence
python -m src.cli timeline
python -m src.cli deps
python -m src.cli mermaid
python -m src.cli roadmap
python -m src.cli risks
python -m src.cli rag
uvicorn src.ui.api:app --reload



pip install -r requirements.txt && python -m src.cli ingest && python -m src.cli cluster && python -m src.cli summarize && python -m src.cli confidence && python -m src.cli timeline && python -m src.cli deps && python -m src.cli mermaid && python -m src.cli roadmap && python -m src.cli risks && python -m src.cli rag && uvicorn src.ui.api:app --reload

pip install -r requirements.txt && python -m src.cli ingest && uvicorn src.ui.api:app --reload

python -m src.cli ingest && uvicorn src.ui.api:app --reload


Every update
python -m src.cli ingest
python -m src.cli cluster

✅ Final result
You now have a local, offline, PM-grade product intelligence platform with:
Semantic project grouping
Decision memory
Risk aging
Roadmap inference
Mermaid graphs
Project comparison
RAG assistant
Web UI
If you want next:
One-command pipeline
Risk heatmaps
Cross-project dependency graph
Weekly PM brief generator
