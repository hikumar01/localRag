from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
from typing import Optional
from tqdm import tqdm
from .state import load_state, save_state, file_hash
from .extractors import extract

INPUT = Path("data/input")
OUT = Path("data/extracted")

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tiff"}
VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi"}

def _extract_worker(path_str: str, skip_ocr: bool, skip_video: bool) -> tuple[str, str]:
    path = Path(path_str)
    text = extract(path, skip_ocr=skip_ocr, skip_video=skip_video)
    return path_str, text

def run(*, skip_ocr: bool = False, skip_video: bool = False, workers: Optional[int] = None):
    state = load_state()
    workers = workers or os.cpu_count() or 1
    to_process: list[tuple[str, str]] = []

    all_files = [p for p in INPUT.rglob("*") if p.is_file()]
    for f in tqdm(all_files, desc="Scan", unit="file"):
        if not f.is_file():
            continue

        ext = f.suffix.lower()
        if skip_ocr and ext in IMAGE_EXTS:
            continue
        if skip_video and ext in VIDEO_EXTS:
            continue

        h = file_hash(f)
        if state.get(str(f)) == h:
            continue

        to_process.append((str(f), h))

    if not to_process:
        return

    with ProcessPoolExecutor(max_workers=workers) as ex:
        futures = {
            ex.submit(_extract_worker, path_str, skip_ocr, skip_video): (path_str, h)
            for path_str, h in to_process
        }
        with tqdm(total=len(futures), desc="Extract", unit="file") as pbar:
            for fut in as_completed(futures):
                path_str, h = futures[fut]
                _path_str, text = fut.result()
                out = (OUT / Path(path_str).relative_to(INPUT)).with_suffix(".txt")
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(text or "")
                state[path_str] = h
                pbar.update(1)

    save_state(state)
