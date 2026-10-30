#!/usr/bin/env python3
"""Read-only HDL project inventory for digital IC skills."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

HDL_SUFFIXES = {".v", ".sv", ".vh", ".svh"}
SKIP_DIRS = {".git", ".hg", ".svn", "build", "dist", "out", "simv.daidir", "work"}
BUILD_NAMES = {
    "Makefile", "makefile", "CMakeLists.txt", "Bazel", "BUILD", "BUILD.bazel",
    "fusesoc.conf", "edalize.conf",
}
BUILD_SUFFIXES = {".f", ".core", ".tcl", ".mk", ".yml", ".yaml", ".toml"}
DECL_RE = re.compile(r"^\s*(module|interface|package)\s+([A-Za-z_][A-Za-z0-9_$]*)", re.MULTILINE)
CLOCK_RE = re.compile(r"\b(?:clk|clock)(?:_[A-Za-z0-9_]+)?\b", re.IGNORECASE)
RESET_RE = re.compile(r"\b(?:rst|reset)(?:_n|n)?(?:_[A-Za-z0-9_]+)?\b", re.IGNORECASE)


def files_under(root: Path):
    found = []
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(name for name in dirs if name not in SKIP_DIRS)
        found.extend(Path(current) / name for name in files)
    yield from sorted(found)


def scan(root: Path) -> dict:
    hdl_files = []
    build_files = []
    declarations = []
    clocks = set()
    resets = set()
    unreadable = []

    for path in files_under(root):
        rel = path.relative_to(root).as_posix()
        if path.name in BUILD_NAMES or path.suffix.lower() in BUILD_SUFFIXES:
            build_files.append(rel)
        if path.suffix.lower() not in HDL_SUFFIXES:
            continue
        hdl_files.append(rel)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            unreadable.append({"file": rel, "error": str(exc)})
            continue
        for kind, name in DECL_RE.findall(text):
            declarations.append({"kind": kind, "name": name, "file": rel})
        clocks.update(CLOCK_RE.findall(text))
        resets.update(RESET_RE.findall(text))

    return {
        "root": str(root.resolve()),
        "hdl_file_count": len(hdl_files),
        "hdl_files": hdl_files,
        "build_files": build_files,
        "declarations": declarations,
        "clock_name_candidates": sorted(clocks, key=str.lower),
        "reset_name_candidates": sorted(resets, key=str.lower),
        "unreadable": unreadable,
        "note": "Candidates are lexical hints; verify clocks, resets, tops and build commands in source/configuration.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory an HDL project without modifying it.")
    parser.add_argument("root", nargs="?", default=".", help="project root")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    result = scan(root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Root: {result['root']}")
        print(f"HDL files: {result['hdl_file_count']}")
        print("Declarations:")
        for item in result["declarations"]:
            print(f"  {item['kind']:9} {item['name']} ({item['file']})")
        print("Build/filelist candidates:")
        for item in result["build_files"]:
            print(f"  {item}")
        print("Clock names: " + (", ".join(result["clock_name_candidates"]) or "none found"))
        print("Reset names: " + (", ".join(result["reset_name_candidates"]) or "none found"))
        print(result["note"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
