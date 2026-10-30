#!/usr/bin/env python3
"""Validate a requirement-traceable digital IC verification-plan CSV."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

REQUIRED = ("id", "requirement", "stimulus", "checker", "coverage", "level", "priority", "status")
STATUSES = {"planned", "implemented", "covered", "waived"}


def validate(path: Path, closure: bool = False) -> dict:
    errors = []
    warnings = []
    rows = []
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            fields = tuple(reader.fieldnames or ())
            if len(set(fields)) != len(fields):
                errors.append("duplicate column names")
            missing = [field for field in REQUIRED if field not in fields]
            if missing:
                errors.append(f"missing columns: {', '.join(missing)}")
            rows = list(reader)
    except (OSError, csv.Error) as exc:
        return {"valid": False, "rows": 0, "errors": [str(exc)], "warnings": []}

    seen = set()
    for line, row in enumerate(rows, start=2):
        if None in row:
            errors.append(f"line {line}: more values than columns")
        row_id = (row.get("id") or "").strip()
        if not row_id:
            errors.append(f"line {line}: empty id")
        elif row_id in seen:
            errors.append(f"line {line}: duplicate id {row_id}")
        seen.add(row_id)
        for field in ("requirement", "stimulus", "checker", "coverage"):
            if field in row and not (row.get(field) or "").strip():
                errors.append(f"line {line} ({row_id or 'no-id'}): empty {field}")
        status = (row.get("status") or "").strip().lower()
        if "status" in row and status not in STATUSES:
            errors.append(f"line {line} ({row_id or 'no-id'}): invalid status {status!r}")
        for field in ("level", "priority"):
            if field in row and not (row.get(field) or "").strip():
                errors.append(f"line {line} ({row_id or 'no-id'}): empty {field}")
        if closure:
            if status not in {"covered", "waived"}:
                errors.append(f"line {line} ({row_id}): closure requires covered or waived")
            required = ("waiver_rationale", "waiver_scope", "waiver_approval") if status == "waived" else ("evidence", "configuration", "tool_version", "result", "checker_selftest", "coverage_hit")
            for field in required:
                if not (row.get(field) or "").strip():
                    errors.append(f"line {line} ({row_id}): closure missing {field}")
            if status == "covered":
                for field in ("result", "checker_selftest"):
                    if (row.get(field) or "").strip().lower() != "pass":
                        errors.append(f"line {line} ({row_id}): {field} must be pass")
                if (row.get("coverage_hit") or "").strip().lower() not in {"yes", "true", "1"}:
                    errors.append(f"line {line} ({row_id}): coverage target not hit")
                evidence=(row.get("evidence") or "").strip()
                if evidence and not (path.parent / evidence).is_file():
                    errors.append(f"line {line} ({row_id}): evidence file does not exist")
                elif evidence and (path.parent / evidence).stat().st_size == 0:
                    errors.append(f"line {line} ({row_id}): evidence file is empty")
        if status == "waived" and not closure:
            warnings.append(f"line {line} ({row_id or 'no-id'}): waiver rationale is not represented by this minimal schema")
        if status == "covered" and (not (row.get("checker") or "").strip() or not (row.get("coverage") or "").strip()):
            errors.append(f"line {line} ({row_id or 'no-id'}): covered requires checker and coverage")

    if not rows:
        (errors if closure else warnings).append("plan has no verification items")
    return {"valid": not errors, "rows": len(rows), "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a verification-plan CSV.")
    parser.add_argument("plan", help="CSV file")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--closure", action="store_true", help="require evidence files, passing checker self-test, coverage hits or documented waivers; metadata validation only")
    args = parser.parse_args()
    result = validate(Path(args.plan), closure=args.closure)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Rows: {result['rows']}  Valid: {'yes' if result['valid'] else 'no'}")
        for item in result["errors"]:
            print(f"ERROR: {item}")
        for item in result["warnings"]:
            print(f"WARN: {item}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
