#!/usr/bin/env python3
"""Write the competition entry: a plan for turning $100 into the most money in 30 days.

Runs with no network. Writes one plan text (1-280 Unicode code points) to
/output/entry.txt, creating /output if needed. Deterministic; finishes in seconds.
"""

import os
import tempfile


def _write_atomic(path, text):
    """Write text atomically: temp file in the same directory, then rename."""
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise

ENTRY = (
    "Day 1: post a $25 AI product-photo cleanup gig on Fiverr, "
    "portfolio: 10 free before/after Etsy edits. "
    "Days 2-30: deliver 2 orders a day ($50/day), "
    "upsell repeat sellers a $49/month retainer. "
    "Likely: ~$1,300 gross, ~$1,100 kept. "
    "Real buyers pay today; no luck, no human needed."
)

OUTPUT_PATH = "/output/entry.txt"


def main():
    # Validate the entry before writing: 1-280 Unicode code points, not blank.
    length = len(ENTRY)
    if not 1 <= length <= 280:
        raise ValueError(f"entry must be 1-280 code points, got {length}")
    if not ENTRY.strip():
        raise ValueError("entry must not be only whitespace")
    _write_atomic(OUTPUT_PATH, ENTRY)


if __name__ == "__main__":
    main()
