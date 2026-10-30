from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scan = load("scan", "skills/digital-ic-rtl-design/scripts/scan_hdl_project.py")
runner = load("runner", "skills/digital-ic-rtl-design/scripts/run_hdl_checks.py")
plan = load("plan", "skills/digital-ic-verification/scripts/check_verification_plan.py")
logs = load("logs", "skills/digital-ic-review-debug/scripts/summarize_diagnostics.py")
installer = load("installer", "scripts/install.py")


class TemporaryCase(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="digital-ic-test-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)


class ScanTests(TemporaryCase):
    def test_project_inventory_and_generated_exclusions(self):
        (self.root / "design.sv").write_text("module fifo(input clk_core, rst_n); endmodule\n", encoding="utf-8")
        (self.root / "Makefile").write_text("smoke:\n", encoding="utf-8")
        (self.root / "build").mkdir()
        (self.root / "build/ignored.sv").write_text("module ignored; endmodule", encoding="utf-8")
        result = scan.scan(self.root)
        self.assertEqual(result["hdl_files"], ["design.sv"])
        self.assertIn("Makefile", result["build_files"])
        self.assertEqual(result["declarations"][0]["name"], "fifo")
        self.assertIn("clk_core", result["clock_name_candidates"])
        self.assertIn("rst_n", result["reset_name_candidates"])


class DiagnosticTests(unittest.TestCase):
    def test_categories_preserve_original_line_and_bounded_samples(self):
        result = logs.classify(["start\n", "WIDTH warning\n", "width mismatch\n", "UVM_ERROR timeout\n"], 1)
        groups = {item["category"]: item for item in result["groups"]}
        self.assertEqual(result["diagnostic_line_count"], 3)
        self.assertEqual(groups["width_or_signedness"]["count"], 2)
        self.assertEqual(groups["width_or_signedness"]["samples"], [{"line": 2, "text": "WIDTH warning"}])
        self.assertIn("timeout_or_deadlock", groups)
        self.assertIn("assertion_or_uvm", groups)

    def test_clean_log_is_not_a_diagnostic(self):
        self.assertEqual(logs.classify(["simulation complete\n"], 3)["groups"], [])


class RunnerTests(TemporaryCase):
    def run_checks(self, checks):
        manifest = self.root / "checks.json"
        manifest.write_text(json.dumps({"checks": checks}), encoding="utf-8")
        output = self.root / "run"
        code = runner.run(manifest, self.root, output)
        return code, json.loads((output / "results.json").read_text(encoding="utf-8"))

    def check(self, name, code="print('checked')", **kwargs):
        return {"name": name, "argv": [sys.executable, "-c", code], **kwargs}

    def test_success_preserves_real_log(self):
        code, result = self.run_checks([self.check("smoke")])
        self.assertEqual(code, 0)
        self.assertTrue(result["required_checks_pass"])
        self.assertEqual(result["checks"][0]["exit_code"], 0)
        self.assertIn("checked", Path(result["checks"][0]["log"]).read_text())

    def test_fail_fast_keeps_unrun_check(self):
        code, result = self.run_checks([self.check("fail", "raise SystemExit(7)"), self.check("later")])
        self.assertEqual(code, 1)
        self.assertEqual(result["checks"][0]["exit_code"], 7)
        self.assertFalse(result["required_checks_pass"])
        self.assertEqual(result["not_run"][0]["name"], "later")
        self.assertFalse((self.root / "run/later.log").exists())

    def test_missing_executable_is_unavailable(self):
        code, result = self.run_checks([{"name": "missing", "argv": [str(self.root / "missing-executable")]}])
        self.assertEqual(code, 1)
        self.assertEqual(result["checks"][0]["status"], "unavailable")

    def test_timeout_is_failure(self):
        code, result = self.run_checks([self.check("slow", "import time; time.sleep(30)", timeout_seconds=0.1)])
        self.assertEqual(code, 1)
        self.assertEqual(result["checks"][0]["status"], "timeout")

    def test_optional_failure_does_not_skip_required_check(self):
        code, result = self.run_checks([self.check("optional", "raise SystemExit(2)", required=False), self.check("required")])
        self.assertEqual(code, 0)
        self.assertEqual([row["status"] for row in result["checks"]], ["fail", "pass"])
        self.assertTrue(result["required_checks_pass"])

    def test_invalid_manifests_are_rejected_before_output(self):
        invalid = [
            [],
            [self.check("../escape")],
            [self.check("duplicate"), self.check("duplicate")],
            [self.check("bad_timeout", timeout_seconds=True)],
            [self.check("bad_timeout", timeout_seconds=0)],
            [self.check("bad_required", required="yes")],
            [{"name": "empty_argv", "argv": []}],
        ]
        for checks in invalid:
            with self.subTest(checks=checks):
                with self.assertRaises(ValueError):
                    self.run_checks(checks)
                self.assertFalse((self.root / "run").exists())

    def test_existing_output_is_not_reused(self):
        (self.root / "run").mkdir()
        with self.assertRaises(FileExistsError):
            self.run_checks([self.check("smoke")])

    def test_pending_check_is_not_reported_as_all_passed(self):
        # Observe the result of check 1 while check 2 is deliberately still running.
        manifest = self.root / "checks.json"
        manifest.write_text(json.dumps({"checks": [self.check("first"), self.check("slow", "import time; time.sleep(30)", timeout_seconds=2)]}), encoding="utf-8")
        process = subprocess.Popen([sys.executable, str(ROOT / "skills/digital-ic-rtl-design/scripts/run_hdl_checks.py"), str(manifest), "--repo", str(self.root), "--out", str(self.root / "run")], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        try:
            self.assertEqual(process.stdout.readline().strip(), "first: pass")
            result = json.loads((self.root / "run/results.json").read_text(encoding="utf-8"))
            self.assertFalse(result["run_finished"])
            self.assertFalse(result["required_checks_pass"])
            self.assertEqual(result["not_run"][0]["name"], "slow")
        finally:
            # Let the runner's own timeout finish and reap its child process.
            process.communicate(timeout=10)


class PlanTests(TemporaryCase):
    def row(self, **kwargs):
        return {"id": "REQ-1", "requirement": "preserve data", "stimulus": "backpressure", "checker": "queue model", "coverage": "stall", "level": "block", "priority": "P1", "status": "planned", **kwargs}

    def write_plan(self, rows):
        path = self.root / "plan.csv"
        fields = list(dict.fromkeys([*plan.REQUIRED, *(key for row in rows for key in row)]))
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def covered(self, **kwargs):
        (self.root / "evidence.log").write_text("checker compared 42 transactions\n", encoding="utf-8")
        return self.row(status="covered", evidence="evidence.log", configuration="depth=3", tool_version="test-fixture", result="pass", checker_selftest="pass", coverage_hit="yes", **kwargs)

    def test_basic_plan(self):
        self.assertTrue(plan.validate(self.write_plan([self.row()]))["valid"])

    def test_duplicate_requirement(self):
        self.assertFalse(plan.validate(self.write_plan([self.row(), self.row()]))["valid"])

    def test_closure_rejects_unfinished_and_empty_plan(self):
        self.assertFalse(plan.validate(self.write_plan([self.row()]), True)["valid"])
        self.assertFalse(plan.validate(self.write_plan([]), True)["valid"])

    def test_closure_accepts_complete_evidence(self):
        self.assertTrue(plan.validate(self.write_plan([self.covered()]), True)["valid"])

    def test_closure_rejects_missing_or_empty_evidence(self):
        row = self.covered()
        path = self.write_plan([row])
        (self.root / "evidence.log").unlink()
        self.assertFalse(plan.validate(path, True)["valid"])
        (self.root / "evidence.log").touch()
        self.assertFalse(plan.validate(path, True)["valid"])

    def test_closure_rejects_failed_checks_and_unhit_coverage(self):
        for field, value in [("result", "fail"), ("checker_selftest", "fail"), ("coverage_hit", "no")]:
            row = self.covered()
            row[field] = value
            with self.subTest(field=field):
                self.assertFalse(plan.validate(self.write_plan([row]), True)["valid"])

    def test_closure_requires_waiver_metadata(self):
        self.assertFalse(plan.validate(self.write_plan([self.row(status="waived")]), True)["valid"])
        row = self.row(status="waived", waiver_rationale="not supported in this configuration", waiver_scope="depth=1", waiver_approval="review-record-1")
        self.assertTrue(plan.validate(self.write_plan([row]), True)["valid"])

    def test_missing_required_columns(self):
        path = self.root / "bad.csv"
        path.write_text("id,status\nREQ-1,covered\n", encoding="utf-8")
        self.assertFalse(plan.validate(path)["valid"])


class InstallerTests(TemporaryCase):
    def test_installs_all_siblings_and_shared_references(self):
        targets = installer.install(self.root / "installed")
        self.assertEqual(len(targets), 3)
        for target in targets:
            self.assertTrue((target / "SKILL.md").is_file())
        reference = self.root / "installed/digital-ic-verification/../digital-ic-rtl-design/references/development-flow.md"
        self.assertTrue(reference.is_file())

    def test_existing_destination_blocks_every_copy(self):
        destination = self.root / "installed"
        existing = destination / installer.SKILLS[-1]
        existing.mkdir(parents=True)
        (existing / "keep.txt").write_text("user changes", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            installer.install(destination)
        self.assertFalse((destination / installer.SKILLS[0]).exists())
        self.assertEqual((existing / "keep.txt").read_text(), "user changes")

    def test_destination_inside_source_is_rejected(self):
        with self.assertRaises(ValueError):
            installer.install(installer.SOURCE / "nested")


if __name__ == "__main__":
    unittest.main()
