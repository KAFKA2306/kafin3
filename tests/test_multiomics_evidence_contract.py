"""Regression checks for the published multiomics evidence contract.

Exercise accepted and rejected artifact sets without contacting external services.
"""

import json
import tempfile
import unittest
from pathlib import Path

from scripts.verify_multiomics import verify


class MultiomicsEvidenceContractTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.payloads = {
            "clinical-trials.json": {
                "coverage_years": 5,
                "study_count": 2,
                "api_version": {"dataTimestamp": "2026-10-01"},
            },
            "sequencing-costs.json": {
                "observations": [
                    {"observation_date": "2020-01-01"},
                    *[{"observation_date": "2022-01-01"} for _ in range(9)],
                ]
            },
            "fda-approvals.json": {
                "approval_count": 1,
                "approvals": [{
                    "source_url": "https://www.accessdata.fda.gov/drugsatfda_docs/example",
                    "omics_modalities": ["unknown"],
                }],
            },
            "summary.json": {
                "clinical_trials": {"study_count": 2},
                "sequencing_costs": {"observation_count": 10},
                "fda_approvals": {"approval_count": 1},
            },
            "manifest.json": {
                "sources": ["clinical_trials_version", "nhgri", "drugs_at_fda"]
            },
        }
        self.write_payloads()

    def write_payloads(self):
        for filename, payload in self.payloads.items():
            (self.root / filename).write_text(
                json.dumps(payload), encoding="utf-8"
            )

    def test_consistent_artifacts_are_accepted(self):
        self.assertIsNone(verify(self.root))

    def test_summary_count_mismatch_is_rejected(self):
        self.payloads["summary.json"]["clinical_trials"]["study_count"] = 99
        self.write_payloads()
        with self.assertRaises(AssertionError):
            verify(self.root)

    def test_unapproved_source_manifest_is_rejected(self):
        self.payloads["manifest.json"]["sources"].append("unverified_source")
        self.write_payloads()
        with self.assertRaises(AssertionError):
            verify(self.root)

    def test_untrusted_approval_url_is_rejected(self):
        self.payloads["fda-approvals.json"]["approvals"][0]["source_url"] = (
            "https://example.invalid/claim"
        )
        self.write_payloads()
        with self.assertRaises(AssertionError):
            verify(self.root)

    def test_missing_artifact_is_not_accepted(self):
        (self.root / "manifest.json").unlink()
        with self.assertRaises(FileNotFoundError):
            verify(self.root)


if __name__ == "__main__":
    unittest.main()
