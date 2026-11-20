"""Verify the versioned inputs for the three November 20 instrument follow-ups."""

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def check():
    frozen = json.loads((HERE / "input_lock.json").read_text())
    for name, expected in frozen.items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"instrument follow-up input changed: {name}")
    return frozen
