from pathlib import Path
import subprocess
import tempfile
import os
import shutil
import logging

import pytesseract
from PIL import Image

import whisper


# --------------------------------------------------
# Logging
# --------------------------------------------------
logger = logging.getLogger(__name__)


# --------------------------------------------------
# Whisper model (lazy loaded)
# --------------------------------------------------
_whisper_model = None


def get_whisper():
    global _whisper_model
    if _whisper_model is None:
        logger.info("Loading Whisper model (tiny)…")
        _whisper_model = whisper.load_model("tiny")
    return _whisper_model

# --------------------------------------------------
# Public API
# --------------------------------------------------
def extract(path: Path, *, skip_ocr: bool = False, skip_video: bool = False) -> str:
    """
    Extract text from a file of various formats.
    Returns extracted text or empty string on failure.
    """
    try:
        ext = path.suffix.lower()

        if ext in [".txt", ".md"]:
            return _read_text(path)

        if ext == ".pdf":
            return _extract_pdf(path)

        if ext in [".doc", ".docx", ".ppt", ".pptx", ".one"]:
            return _extract_office(path)

        if ext in [".png", ".jpg", ".jpeg", ".tiff"]:
            if skip_ocr:
                return ""
            return _extract_image(path)

        if ext in [".mp4", ".mov", ".mkv", ".avi"]:
            if skip_video:
                return ""
            return _extract_video_audio(path)

        if ext in [".fig", ".xd"]:
            return _read_text(path)

        logger.warning(f"Unsupported file type: {path}")
        return ""

    except Exception as e:
        logger.exception(f"Failed to extract {path}: {e}")
        return ""


# --------------------------------------------------
# Helpers
# --------------------------------------------------
def _read_text(path: Path) -> str:
    return path.read_text(errors="ignore")


def _extract_pdf(path: Path) -> str:
    if not _cmd_exists("pdftotext"):
        raise RuntimeError("pdftotext not installed")

    result = subprocess.run(
        ["pdftotext", str(path), "-"],
        capture_output=True,
        text=True,
    )
    return result.stdout


def _extract_office(path: Path) -> str:
    if not _cmd_exists("pandoc"):
        raise RuntimeError("pandoc not installed")

    result = subprocess.run(
        ["pandoc", str(path), "-t", "plain"],
        capture_output=True,
        text=True,
    )
    return result.stdout


def _extract_image(path: Path) -> str:
    return pytesseract.image_to_string(Image.open(path))


def _extract_video_audio(video_path: Path) -> str:
    if not _cmd_exists("ffmpeg"):
        raise RuntimeError("ffmpeg not installed")

    model = get_whisper()

    with tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    ) as tmp:
        wav_path = tmp.name

    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i", str(video_path),
                "-ac", "1",
                "-ar", "16000",
                wav_path,
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        result = model.transcribe(wav_path)
        return result.get("text", "")

    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)


def _cmd_exists(cmd: str) -> bool:
    return shutil.which(cmd) is not None
