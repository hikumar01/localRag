from pathlib import Path
from tqdm import tqdm
from .state import load_state, save_state, file_hash
from .extractors import extract

INPUT = Path("data/input")
OUT = Path("data/extracted")

def run():
    state = load_state()

    for f in tqdm(INPUT.rglob("*")):
        if not f.is_file():
            continue

        h = file_hash(f)
        if state.get(str(f)) == h:
            continue

        text = extract(f)
        out = (OUT / f.relative_to(INPUT)).with_suffix(".txt")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text or "")

        state[str(f)] = h

    save_state(state)
