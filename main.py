#!/usr/bin/env python3
"""Write the competition entry: a plan for turning $100 into the most money in 30 days.

Runs with no network. Writes one plan text (1-280 Unicode code points) to
/output/entry.txt, creating /output if needed. Deterministic; finishes in seconds.
"""

import os

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
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(ENTRY)


if __name__ == "__main__":
    main()
