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
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, path)
        dir_fd = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
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

def verify_output(path, text):
    """Read the written file back and confirm it is valid and world-readable.

    Raises loudly if anything is wrong: missing file, wrong content, entry
    outside the 1-280 code-point rule, or a mode the grader cannot read.
    """
    if not os.path.isfile(path):
        raise RuntimeError(f"output file missing after write: {path}")
    with open(path, "r", encoding="utf-8") as f:
        actual = f.read()
    if actual != text:
        raise RuntimeError("output file content differs from the planned entry")
    if not 1 <= len(actual) <= 280:
        raise ValueError(
            f"written entry must be 1-280 code points, got {len(actual)}"
        )
    if not actual.strip():
        raise ValueError("written entry must not be only whitespace")
    mode = os.stat(path).st_mode & 0o777
    if mode & 0o004 == 0:
        raise RuntimeError(
            f"output file {path} is not world-readable (mode {mode:03o}); "
            "the grader collects it as a different user"
        )


OUTPUT_PATH = os.path.join(
    os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.txt"
)


def main():
    # Validate the entry before writing: 1-280 Unicode code points, not blank.
    length = len(ENTRY)
    if not 1 <= length <= 280:
        raise ValueError(f"entry must be 1-280 code points, got {length}")
    if not ENTRY.strip():
        raise ValueError("entry must not be only whitespace")
    _write_atomic(OUTPUT_PATH, ENTRY)
    verify_output(OUTPUT_PATH, ENTRY)


if __name__ == "__main__":
    main()
