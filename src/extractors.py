from pathlib import Path
import subprocess
import pytesseract
from PIL import Image
import whisper

_whisper_model = None

def get_whisper():
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model("tiny")
    return _whisper_model

def extract(path: Path) -> str:
    ext = path.suffix.lower()

    if ext in [".txt", ".md"]:
        return path.read_text(errors="ignore")

    if ext == ".pdf":
        return subprocess.getoutput(f"pdftotext '{path}' -")

    if ext in [".doc", ".docx", ".ppt", ".pptx", ".one"]:
        return subprocess.getoutput(f"pandoc '{path}' -t plain")

    if ext in [".png", ".jpg", ".jpeg"]:
        return pytesseract.image_to_string(Image.open(path))

    if ext in [".mp4", ".mov", ".mkv"]:
        audio = f"/tmp/{path.stem}.wav"
        subprocess.call(
            ["ffmpeg", "-i", path, audio, "-y"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        model = get_whisper()
        return model.transcribe(audio)["text"]

    if ext in [".fig", ".xd"]:
        return path.read_text(errors="ignore")

    return ""
