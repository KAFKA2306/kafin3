import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.verify_multiomics import verify


ROOT = Path(__file__).resolve().parents[1]


class MultiomicsWorkflowContractTest(unittest.TestCase):
    def test_verification_precedes_commit_and_uses_shared_contract(self):
        source = (ROOT / ".github/workflows/multiomics-source.yml").read_text()
        ci = (ROOT / ".github/workflows/ci.yml").read_text()
        verify_cmd = "python scripts/verify_multiomics.py"
        self.assertIn("python -m unittest discover -s tests -v", source)
        self.assertLess(source.index(verify_cmd), source.index("name: Commit changed evidence"))
        self.assertIn(verify_cmd, ci)

    def test_contract_failure_is_fail_closed(self):
        src = ROOT / "api/v1/multiomics"
        with tempfile.TemporaryDirectory() as tmp:
            dst = Path(tmp)
            for name in (
                "clinical-trials.json",
                "sequencing-costs.json",
                "fda-approvals.json",
                "summary.json",
                "manifest.json",
            ):
                payload = json.loads((src / name).read_text())
                (dst / name).write_text(json.dumps(payload))
            trials_path = dst / "clinical-trials.json"
            trials = json.loads(trials_path.read_text())
            trials["study_count"] = 0
            trials_path.write_text(json.dumps(trials))
            with self.assertRaises(AssertionError):
                verify(dst)


if __name__ == "__main__":
    unittest.main()
