#!/usr/bin/env python3
"""Deliver the 21 November 2026 front page to the grader's output folder.

The picture itself is drawn ahead of time (see draw_news.py) and kept in
this repository as entry.png: 48 stories from seven regions in one
1024x1024 picture. This entrypoint only moves those bytes into the
directory the grader names, so the graded run needs no network,
no fonts and no Pillow -- and it always writes exactly the same file.
"""

import os
import shutil
from pathlib import Path


def deliver() -> Path:
    """Copy entry.png into the output directory; return its new path."""
    repo_root = Path(__file__).resolve().parent
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    destination = target_dir / "entry.png"
    shutil.copyfile(repo_root / "entry.png", destination)
    return destination


if __name__ == "__main__":
    deliver()
