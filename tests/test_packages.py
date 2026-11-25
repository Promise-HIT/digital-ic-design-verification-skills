import posixpath
import subprocess
import sys
import tempfile
import unittest
from itertools import product
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from package_skills import LINK, SKILLS, curriculum


class PackageTests(unittest.TestCase):
    def test_individual_archives_resolve_links_without_other_skills(self):
        with tempfile.TemporaryDirectory() as temp:
            subprocess.run([sys.executable, str(ROOT / "scripts/package_skills.py"), "--out", temp], check=True)
            for platform, name in product(("chatgpt", "claude"), SKILLS):
                with self.subTest(platform=platform, skill=name), ZipFile(Path(temp) / f"{platform}-{name}.zip") as z:
                    self.assertEqual(name + "/agents/openai.yaml" in z.namelist(), platform == "chatgpt")
                    self.assertIn(name + "/SKILL.md", z.namelist())
                    for member in z.namelist():
                        self.assertTrue(member.startswith(name + "/"))
                        if not member.endswith(".md"):
                            continue
                        for match in LINK.finditer(z.read(member).decode()):
                            url = urlsplit(match[2])
                            if url.scheme or url.netloc or not url.path:
                                continue
                            target = posixpath.normpath(posixpath.join(posixpath.dirname(member), unquote(url.path)))
                            self.assertIn(target, z.namelist(), (member, match[2]))

    def test_dsh_lessons_match_current_sources(self):
        for name in SKILLS:
            p = ROOT / "deepseek-harness/curriculum" / name / "SKILL.md"
            self.assertEqual(p.read_text(encoding="utf-8"), curriculum(name))

    def test_dsh_executable_resources_match_skill(self):
        name = "digital-ic-eda"
        for resource in ("assets/vivado-checkpoint-reports.tcl", "scripts/read_uvm_summary.py"):
            source = ROOT / "skills" / name / resource
            packed = ROOT / "deepseek-harness/curriculum" / name / resource
            self.assertEqual(source.read_text("utf-8"), packed.read_text("utf-8"))
