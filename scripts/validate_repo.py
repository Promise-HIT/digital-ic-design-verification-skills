#!/usr/bin/env python3
"""Validate skill metadata, repository links and Python syntax without EDA tools."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"digital-ic-rtl-design", "digital-ic-verification", "digital-ic-review-debug"}
LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")


def validate(root: Path = ROOT) -> tuple[list[str], dict[str, int]]:
    root = root.resolve()
    errors = []
    counts = {"skills": 0, "local_links": 0, "python_files": 0, "json_files": 0}
    skills = {path.name for path in (root / "skills").iterdir() if path.is_dir()}
    if skills != EXPECTED:
        errors.append(f"expected three skill directories, found {sorted(skills)}")
    for name in sorted(EXPECTED):
        entry = root / "skills" / name / "SKILL.md"
        try:
            text = entry.read_text(encoding="utf-8")
            match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
            if not match:
                raise ValueError("missing YAML frontmatter")
            meta = yaml.safe_load(match.group(1))
            if not isinstance(meta, dict) or meta.get("name") != name:
                raise ValueError("frontmatter name must match directory")
            description = meta.get("description")
            if not isinstance(description, str) or not description.strip() or len(description) > 1024:
                raise ValueError("description must be a nonempty string of at most 1024 characters")
            ui = yaml.safe_load((entry.parent / "agents/openai.yaml").read_text(encoding="utf-8"))
            interface = ui["interface"]
            for field in ("display_name", "short_description", "default_prompt"):
                if not isinstance(interface.get(field), str) or not interface[field].strip():
                    raise ValueError(f"missing UI field: {field}")
            if f"${name}" not in interface["default_prompt"]:
                raise ValueError("default prompt must mention its skill")
            counts["skills"] += 1
        except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError) as exc:
            errors.append(f"{entry.relative_to(root)}: {exc}")

    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in {".git", ".venv", "__pycache__"} for part in relative.parts) or not path.is_file():
            continue
        try:
            if path.suffix in {".md", ".py", ".json", ".yaml", ".yml", ".csv", ".txt"}:
                text = path.read_text(encoding="utf-8")
                # Actual personal paths are not portable publication material.
                if re.search(r"[A-Za-z]:[\\/]+(?:Users|XuNuo)[\\/]", text, re.I):
                    errors.append(f"{relative}: personal absolute path")
            if path.suffix == ".md":
                for target in LINK.findall(text):
                    target = target.strip().strip("<>")
                    parsed = urlsplit(target)
                    if parsed.scheme or parsed.netloc or not parsed.path:
                        continue
                    resolved = (path.parent / unquote(parsed.path)).resolve()
                    if not resolved.is_relative_to(root) or not resolved.exists():
                        errors.append(f"{relative}: invalid local link {target}")
                    counts["local_links"] += 1
            elif path.suffix == ".py":
                ast.parse(text, filename=str(relative))
                counts["python_files"] += 1
            elif path.suffix == ".json":
                json.loads(text)
                counts["json_files"] += 1
            elif path.suffix in {".yaml", ".yml"}:
                yaml.safe_load(text)
        except (OSError, ValueError, SyntaxError, yaml.YAMLError) as exc:
            errors.append(f"{relative}: {exc}")
    return errors, counts


if __name__ == "__main__":
    issues, summary = validate()
    print(json.dumps({"valid": not issues, **summary, "errors": issues}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(issues))
