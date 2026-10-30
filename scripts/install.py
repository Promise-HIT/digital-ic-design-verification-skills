#!/usr/bin/env python3
"""Copy the three related skills into an explicitly selected directory."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

SKILLS = (
    "digital-ic-rtl-design",
    "digital-ic-verification",
    "digital-ic-review-debug",
)
SOURCE = Path(__file__).resolve().parents[1] / "skills"


def install(destination: Path) -> list[Path]:
    destination = destination.expanduser().resolve()
    if destination == SOURCE or SOURCE in destination.parents:
        raise ValueError("destination must be outside the source skills directory")
    targets = [destination / name for name in SKILLS]
    for name, target in zip(SKILLS, targets):
        if not (SOURCE / name / "SKILL.md").is_file():
            raise ValueError(f"source skill is incomplete: {name}")
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"refusing to overwrite existing destination: {target}")
    destination.mkdir(parents=True, exist_ok=True)
    for name, target in zip(SKILLS, targets):
        shutil.copytree(SOURCE / name, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return targets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, required=True, help="explicit parent directory for all three skills")
    args = parser.parse_args()
    try:
        for target in install(args.dest):
            print(f"Installed: {target}")
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Installation failed: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
