import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_multiomics_summary as MODULE


class MultiomicsSummaryTest(unittest.TestCase):
    def test_summary_keeps_counts_and_latest_cost_without_copying_ledgers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "clinical-trials.json").write_text(
                json.dumps(
                    {
                        "api_version": {"dataTimestamp": "2026-08-18T09:00:05"},
                        "coverage_years": 5,
                        "study_count": 2569,
                        "first_study_posted": "2021-08-20",
                        "last_study_posted": "2026-08-18",
                        "modality_counts": {"genomics": 100},
                        "studies": [{"nct_id": "NCT1"}],
                    }
                ),
                encoding="utf-8",
            )
            (root / "sequencing-costs.json").write_text(
                json.dumps(
                    {
                        "source_url": "https://www.genome.gov/example.xls",
                        "observations": [
                            {
                                "observation_date": "2021-01-01",
                                "cost_per_megabase_usd": 0.01,
                                "cost_per_genome_usd": 600,
                            },
                            {
                                "observation_date": "2022-01-01",
                                "cost_per_megabase_usd": 0.005,
                                "cost_per_genome_usd": 500,
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (root / "fda-approvals.json").write_text(
                json.dumps(
                    {
                        "coverage_years": 5,
                        "approval_count": 25307,
                        "source_url": "https://www.fda.gov/example.zip",
                        "approvals": [{"application_number": "1"}],
                    }
                ),
                encoding="utf-8",
            )

            summary = MODULE.build(root)

        self.assertEqual(summary["clinical_trials"]["study_count"], 2569)
        self.assertEqual(summary["sequencing_costs"]["observation_count"], 2)
        self.assertEqual(
            summary["sequencing_costs"]["latest"]["cost_per_genome_usd"], 500
        )
        self.assertEqual(summary["fda_approvals"]["approval_count"], 25307)
        self.assertNotIn("studies", summary["clinical_trials"])
        self.assertNotIn("approvals", summary["fda_approvals"])


if __name__ == "__main__":
    unittest.main()
