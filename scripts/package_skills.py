"""Build individually installable skill archives and refresh the dsh curriculum."""

from __future__ import annotations

import argparse
import os
import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from install import SKILLS, SOURCE

ROOT = SOURCE.parent
LINK = re.compile(r"(!?\[[^\]\n]*\]\()([^)\n]+)(\))")
# The dsh host returns the registered Markdown body, including offline lessons.
LESSONS = {
    "digital-ic-rtl-design": ("agent-rtl", "fsm-worked-example"),
    "digital-ic-verification": ("agent-testbench", "bench-worked-example"),
    "digital-ic-review-debug": ("course-triage", "report-worked-example"),
    "digital-ic-amba": ("apb", "ahb", "axi"),
    "digital-ic-eda": ("frontend", "implementation", "automation", "manuals"),
}


def curriculum(name: str) -> str:
    base = SOURCE / name
    header, body = (base / "SKILL.md").read_text(encoding="utf-8").split("\n---\n", 1)
    lessons = LESSONS[name]
    parts = [(base / "references" / (item + ".md")).read_text(encoding="utf-8").strip() for item in lessons]
    if name in {"digital-ic-amba", "digital-ic-eda"}:
        # Inline the referenced chapters in place of the file-based router.
        parts.insert(0, "\n".join(line for line in body.splitlines() if not line.startswith("- ")).strip())
    content = "\n\n".join(parts)
    if name == "digital-ic-eda":
        content = content.replace("](../scripts/", "](scripts/").replace("](../assets/", "](assets/")
    return header + "\n---\n\n" + content + "\n"


def skill_files(name: str, platform: str) -> dict[str, bytes]:
    """Vendor linked sibling references so a single uploaded ZIP works on its own."""
    base = SOURCE / name
    pending = [p for p in base.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"]
    files = {}

    def location(p: Path) -> Path:
        if p.is_relative_to(base):
            return Path(name) / p.relative_to(base)
        return Path(name, "related") / p.relative_to(SOURCE)

    while pending:
        p = pending.pop()
        if platform == "claude" and p == base / "agents/openai.yaml":
            continue
        member = location(p)
        if member.as_posix() in files:
            continue
        if p.suffix == ".md":
            def relocate(match: re.Match) -> str:
                url = urlsplit(match[2])
                if url.scheme or url.netloc or not url.path:
                    return match[0]
                target = (p.parent / unquote(url.path)).resolve()
                if not target.is_relative_to(SOURCE) or not target.is_file():
                    raise ValueError(f"Broken package reference in {p}: {match[2]}")
                pending.append(target)
                rel = Path(os.path.relpath(location(target), member.parent)).as_posix()
                return match[1] + url._replace(path=rel).geturl() + match[3]

            data = LINK.sub(relocate, p.read_text(encoding="utf-8")).encode()
        elif p.suffix in {".yaml", ".json", ".py", ".csv"}:
            data = p.read_text(encoding="utf-8").encode()
        else:
            data = p.read_bytes()
        files[member.as_posix()] = data
    files[f"{name}/LICENSE"] = (ROOT / "LICENSE").read_text(encoding="utf-8").encode()
    return files


def archive(name: str, output: Path, platform: str) -> Path:
    output.mkdir(exist_ok=True, parents=True)
    path = output / f"{platform}-{name}.zip"
    files = skill_files(name, platform)
    with ZipFile(path, "w") as z:
        for member, data in sorted(files.items()):
            info = ZipInfo(member)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, data, compress_type=ZIP_DEFLATED)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="write standalone ZIPs to this directory")
    parser.add_argument("--sync-dsh", action="store_true", help="regenerate the checked-in plugin lessons")
    args = parser.parse_args()
    if not (args.out or args.sync_dsh):
        parser.error("select --out and/or --sync-dsh")
    for name in SKILLS:
        if args.sync_dsh:
            destination = ROOT / "deepseek-harness/curriculum" / name / "SKILL.md"
            destination.parent.mkdir(exist_ok=True, parents=True)
            destination.write_text(curriculum(name), encoding="utf-8", newline="\n")
            if name == "digital-ic-eda":
                for subdir in ("assets", "scripts"):
                    shutil.copytree(SOURCE / name / subdir, destination.parent / subdir,
                                    dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        if args.out:
            for platform in ("chatgpt", "claude"):
                print(archive(name, args.out, platform))


if __name__ == "__main__":
    main()
