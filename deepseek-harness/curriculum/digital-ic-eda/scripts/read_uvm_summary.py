"""Read one standard UVM report-server summary from one simulation transcript."""

import argparse
import json
from pathlib import Path
import re

HEADER = re.compile(r"^\s*(?:#\s*)?---\s*UVM Report Summary\s*---\s*$")
COUNT = re.compile(r"^\s*(?:#\s*)?UVM_(ERROR|FATAL)\s*:\s*(\d+)\s*$")


def inspect(lines):
    headers = 0
    counts = {}
    repeated = False
    for number, line in enumerate(lines, 1):
        if HEADER.match(line):
            headers += 1
            continue
        match = COUNT.match(line)
        if headers and match:
            kind, value = match.groups()
            repeated |= kind in counts
            counts[kind] = {"count": int(value), "line": number}
    if headers != 1 or repeated or set(counts) != {"ERROR", "FATAL"}:
        status = "incomplete_or_ambiguous"
    elif any(row["count"] for row in counts.values()):
        status = "reported_errors"
    else:
        status = "zero_summary_errors"
    return {"status": status, "headers": headers, "severities": counts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("transcript", type=Path)
    args = parser.parse_args()
    with args.transcript.open(encoding="utf-8-sig", errors="replace") as stream:
        result = inspect(stream)
    print(json.dumps(result, indent=2))
    return {"zero_summary_errors": 0, "reported_errors": 1, "incomplete_or_ambiguous": 2}[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
