import unittest

from scripts.collect_clinical_trials import normalize


class NormalizeStudyTest(unittest.TestCase):
    def test_keeps_trial_identity_and_evidence_fields(self):
        study = {
            "protocolSection": {
                "identificationModule": {"nctId": "NCT00000001", "briefTitle": "Genomics study"},
                "statusModule": {"overallStatus": "RECRUITING", "startDateStruct": {"date": "2026-01"}},
                "designModule": {
                    "studyType": "INTERVENTIONAL",
                    "phases": ["PHASE2"],
                    "enrollmentInfo": {"count": 42, "type": "ESTIMATED"},
                },
                "sponsorCollaboratorsModule": {"leadSponsor": {"name": "Example University", "class": "OTHER"}},
                "conditionsModule": {"conditions": ["Cancer"]},
                "armsInterventionsModule": {
                    "interventions": [{"type": "DIAGNOSTIC_TEST", "name": "RNA sequencing"}]
                },
            }
        }
        row = normalize(study)
        self.assertEqual(row["nct_id"], "NCT00000001")
        self.assertEqual(row["phases"], ["PHASE2"])
        self.assertEqual(row["lead_sponsor"], "Example University")
        self.assertEqual(row["interventions"][0]["name"], "RNA sequencing")


if __name__ == "__main__":
    unittest.main()
