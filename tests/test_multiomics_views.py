import importlib.util
import io
import sys
import unittest
import zipfile
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location("update_multiomics", ROOT / "scripts" / "update_multiomics.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


def make_drugs_zip() -> bytes:
    out = io.BytesIO()
    approved = date.today().strftime("%Y%m%d")
    with zipfile.ZipFile(out, "w") as archive:
        archive.writestr("Applications.txt", "ApplNo\tApplType\tSponsorName\n000001\tNDA\tExample Sponsor\n")
        archive.writestr(
            "Products.txt",
            "ApplNo\tProductNo\tForm\tStrength\tDrugName\tActiveIngredient\n"
            "000001\t001\tTABLET\t10MG\tEXAMPLE\tEXAMPLINE\n",
        )
        archive.writestr(
            "Submissions.txt",
            "ApplNo\tSubmissionClassCodeID\tSubmissionType\tSubmissionNo\tSubmissionStatus\tSubmissionStatusDate\tSubmissionsPublicNotes\tReviewPriority\n"
            f"000001\t\tORIG\t1\tAP\t{approved}\t\tPriority\n",
        )
    return out.getvalue()


class MultiomicsViewsTest(unittest.TestCase):
    def test_fda_approval_keeps_official_identity_without_modality_inference(self):
        rows = MODULE.parse_fda_zip(make_drugs_zip(), years=5)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["application_number"], "000001")
        self.assertEqual(rows[0]["omics_modalities"], ["unknown"])
        self.assertIn("ApplNo=000001", rows[0]["source_url"])

    def test_trial_coverage_is_date_bounded(self):
        recent = (date.today() - timedelta(days=30)).isoformat()
        old = (date.today() - timedelta(days=365 * 8)).isoformat()
        studies = [
            {"nct_id": "NCT1", "study_first_posted": recent, "omics_modalities": ["genomics"]},
            {"nct_id": "NCT2", "study_first_posted": old, "omics_modalities": ["unknown"]},
        ]
        view = MODULE.trial_coverage(studies, 5)
        self.assertEqual(view["study_count"], 1)
        self.assertEqual(view["modality_counts"], {"genomics": 1})

    def test_parse_date_accepts_fda_and_iso_dates(self):
        self.assertEqual(MODULE.parse_date("20260729"), "2026-07-29")
        self.assertEqual(MODULE.parse_date("07/29/2026"), "2026-07-29")
        self.assertEqual(MODULE.parse_date("2026-07-29"), "2026-07-29")


if __name__ == "__main__":
    unittest.main()
