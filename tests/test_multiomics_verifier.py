import json
import tempfile
import unittest
from pathlib import Path

from scripts.verify_multiomics import verify_multiomics_root


class MultiomicsVerifierTest(unittest.TestCase):
    def _write_fixture(self, root: Path) -> None:
        trials = {
            "coverage_years": 5,
            "study_count": 1,
            "api_version": {"dataTimestamp": "2026-09-01"},
        }
        costs = {
            "observations": [
                {"observation_date": "2020-01-01"},
                *({"observation_date": "2022-01-01"} for _ in range(9)),
            ]
        }
        approvals = {
            "approval_count": 1,
            "approvals": [{
                "source_url": "https://www.accessdata.fda.gov/example",
                "omics_modalities": ["unknown"],
            }],
        }
        summary = {
            "clinical_trials": {"study_count": 1},
            "sequencing_costs": {"observation_count": 10},
            "fda_approvals": {"approval_count": 1},
        }
        manifest = {
            "sources": ["clinical_trials_version", "nhgri", "drugs_at_fda"]
        }
        for name, payload in {
            "clinical-trials.json": trials,
            "sequencing-costs.json": costs,
            "fda-approvals.json": approvals,
            "summary.json": summary,
            "manifest.json": manifest,
        }.items():
            (root / name).write_text(json.dumps(payload), encoding="utf-8")

    def test_valid_fixture_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_fixture(root)
            result = verify_multiomics_root(root)
            self.assertEqual(result["sequencing_cost_observations"], 10)

    def test_contract_failure_is_not_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_fixture(root)
            summary_path = root / "summary.json"
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            summary["clinical_trials"]["study_count"] = 999
            summary_path.write_text(json.dumps(summary), encoding="utf-8")
            with self.assertRaises(AssertionError):
                verify_multiomics_root(root)


class WorkflowContractTest(unittest.TestCase):
    def test_source_refresh_verifies_before_commit(self):
        workflow = Path(".github/workflows/multiomics-source.yml").read_text(
            encoding="utf-8"
        )
        tests_pos = workflow.index("python -m unittest discover -s tests -v")
        verify_pos = workflow.index("python scripts/verify_multiomics.py")
        commit_pos = workflow.index("- name: Commit changed evidence")
        self.assertLess(tests_pos, commit_pos)
        self.assertLess(verify_pos, commit_pos)

    def test_ci_and_source_use_same_artifact_verifier(self):
        source = Path(".github/workflows/multiomics-source.yml").read_text(
            encoding="utf-8"
        )
        ci = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
        command = "python scripts/verify_multiomics.py"
        self.assertIn(command, source)
        self.assertIn(command, ci)


if __name__ == "__main__":
    unittest.main()
