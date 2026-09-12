import json
import tempfile
import unittest
from pathlib import Path

from scripts.verify_multiomics import VerificationError, verify


class VerifyMultiomicsTest(unittest.TestCase):
    def test_rejects_summary_count_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            observations = [
                {"observation_date": f"20{10 + i:02d}-01-01"} for i in range(10)
            ]
            payloads = {
                "clinical-trials.json": {
                    "coverage_years": 5,
                    "study_count": 1,
                    "api_version": {"dataTimestamp": "2026-09-12T00:00:00Z"},
                },
                "sequencing-costs.json": {"observations": observations},
                "fda-approvals.json": {
                    "approval_count": 1,
                    "approvals": [
                        {
                            "source_url": "https://www.accessdata.fda.gov/example",
                            "omics_modalities": ["unknown"],
                        }
                    ],
                },
                "summary.json": {
                    "clinical_trials": {"study_count": 2},
                    "sequencing_costs": {"observation_count": 10},
                    "fda_approvals": {"approval_count": 1},
                },
                "manifest.json": {
                    "sources": {
                        "clinical_trials_version": {},
                        "nhgri": {},
                        "drugs_at_fda": {},
                    }
                },
            }
            for name, payload in payloads.items():
                (root / name).write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaisesRegex(VerificationError, "clinical trial count"):
                verify(root)


if __name__ == "__main__":
    unittest.main()
