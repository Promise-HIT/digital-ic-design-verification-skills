import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import json

SCRIPT = Path(__file__).resolve().parents[1] / "skills/digital-ic-eda/scripts/read_uvm_summary.py"
HEADER = "--- UVM Report Summary ---"


class SummaryTests(unittest.TestCase):
    def test_summary_statuses_and_source_locations(self):
        with tempfile.TemporaryDirectory() as temp:
            log = Path(temp) / "run.log"
            for lines, code, status in [
                (["# " + HEADER, "# UVM_ERROR : 0", "# UVM_FATAL : 0"], 0, "zero_summary_errors"),
                ([HEADER, "UVM_ERROR : 2", "UVM_FATAL : 0"], 1, "reported_errors"),
                ([HEADER, "UVM_ERROR : 0"], 2, "incomplete_or_ambiguous"),
                ([HEADER, "UVM_ERROR : 0", "UVM_FATAL : 0", HEADER], 2, "incomplete_or_ambiguous"),
                (["UVM_ERROR : 0", "UVM_FATAL : 0"], 2, "incomplete_or_ambiguous"),
            ]:
                with self.subTest(lines=lines):
                    log.write_text("\n".join(lines), encoding="utf-8")
                    run = subprocess.run([sys.executable, str(SCRIPT), str(log)], capture_output=True, text=True)
                    self.assertEqual(run.returncode, code)
                    result = json.loads(run.stdout)
                    self.assertEqual(result["status"], status)
                    if code < 2:
                        self.assertEqual(result["severities"]["ERROR"]["line"], 2)
