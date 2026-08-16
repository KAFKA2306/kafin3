from scripts.collect_clinical_trials import normalize


def test_normalize_keeps_trial_identity_and_evidence_fields():
    study = {
        "protocolSection": {
            "identificationModule": {"nctId": "NCT00000001", "briefTitle": "Genomics study"},
            "statusModule": {"overallStatus": "RECRUITING", "startDateStruct": {"date": "2026-01"}},
            "designModule": {"studyType": "INTERVENTIONAL", "phases": ["PHASE2"], "enrollmentInfo": {"count": 42, "type": "ESTIMATED"}},
            "sponsorCollaboratorsModule": {"leadSponsor": {"name": "Example University", "class": "OTHER"}},
            "conditionsModule": {"conditions": ["Cancer"]},
            "armsInterventionsModule": {"interventions": [{"type": "DIAGNOSTIC_TEST", "name": "RNA sequencing"}]},
        }
    }
    row = normalize(study)
    assert row["nct_id"] == "NCT00000001"
    assert row["phases"] == ["PHASE2"]
    assert row["lead_sponsor"] == "Example University"
    assert row["interventions"][0]["name"] == "RNA sequencing"
