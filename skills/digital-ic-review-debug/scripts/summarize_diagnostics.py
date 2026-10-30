#!/usr/bin/env python3
"""Group common HDL diagnostics while preserving first actionable samples."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

CATEGORIES = (
    ("syntax_or_elaboration", re.compile(r"syntax error|parse error|elaborat|unresolved|unknown module|undefined", re.I)),
    ("width_or_signedness", re.compile(r"width|truncat|extend|signed|unsigned|selrange|widthexpand", re.I)),
    ("latch_or_combinational", re.compile(r"latch|combinational loop|unoptimizable|always_comb|alwcomborder", re.I)),
    ("multiple_drivers", re.compile(r"multiple driver|multiply driven|blkandnblk|multi[- ]?driven", re.I)),
    ("clock_reset_cdc", re.compile(r"\bcdc\b|\brdc\b|metastab|synchroni[sz]|reset crossing|clock crossing", re.I)),
    ("timing", re.compile(r"setup|hold|slack|timing violation|unconstrained path", re.I)),
    ("assertion_or_uvm", re.compile(r"assertion|\bUVM_(?:FATAL|ERROR)\b|scoreboard|mismatch", re.I)),
    ("timeout_or_deadlock", re.compile(r"timeout|deadlock|watchdog|objection.*not.*drop", re.I)),
    ("coverage", re.compile(r"coverage|uncovered|coverpoint|covergroup", re.I)),
)
GENERIC_ERROR = re.compile(r"\berror\b|\bfatal\b|\bwarning\b", re.I)


def classify(lines: list[str], max_samples: int) -> dict:
    counts = defaultdict(int)
    samples = defaultdict(list)
    matched_lines = set()
    for number, raw in enumerate(lines, start=1):
        line = raw.rstrip("\n")
        categories = [name for name, pattern in CATEGORIES if pattern.search(line)]
        if not categories and GENERIC_ERROR.search(line):
            categories = ["other_diagnostic"]
        for category in categories:
            counts[category] += 1
            matched_lines.add(number)
            if len(samples[category]) < max_samples:
                samples[category].append({"line": number, "text": line[:500]})
    ordered = []
    order = [name for name, _ in CATEGORIES] + ["other_diagnostic"]
    for category in order:
        if counts[category]:
            ordered.append({"category": category, "count": counts[category], "samples": samples[category]})
    return {
        "line_count": len(lines),
        "diagnostic_line_count": len(matched_lines),
        "groups": ordered,
        "note": "Pattern grouping is triage only. Inspect the earliest causal diagnostic and surrounding log context.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize HDL/verification diagnostics.")
    parser.add_argument("log", help="text log")
    parser.add_argument("--max-samples", type=int, default=3, help="samples per category")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()
    if args.max_samples < 1:
        parser.error("--max-samples must be at least 1")
    try:
        lines = Path(args.log).read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    except OSError as exc:
        parser.error(str(exc))
    result = classify(lines, args.max_samples)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Lines: {result['line_count']}  Diagnostic lines: {result['diagnostic_line_count']}")
        for group in result["groups"]:
            print(f"{group['category']}: {group['count']}")
            for sample in group["samples"]:
                print(f"  L{sample['line']}: {sample['text']}")
        print(result["note"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
