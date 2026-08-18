# kafin3 — multiomics evidence collector

`kafin3` is being rebuilt as a small, evidence-first repository for multiomics research data. The legacy finance dashboard, Streamlit/FastAPI prototypes, and their JavaScript/Python dependency stacks are not supported interfaces.

## Current verified scope

The current executable capability is a ClinicalTrials.gov API v2 collector:

```bash
python scripts/collect_clinical_trials.py --pages 1 --page-size 100
```

It records API version metadata, retrieval time, source-page URLs and SHA-256 hashes, and normalized study fields including NCT ID, phase, status, dates, sponsor, enrollment, conditions, and interventions.

ClinicalTrials.gov documents `/api/v2/studies` as the modern study endpoint and `/api/v2/version` as the source for API version and `dataTimestamp`.

Primary source: https://clinicaltrials.gov/data-api/api

## Tests

```bash
python -m unittest discover -s tests -v
```

The test suite uses only the Python standard library.

## Repository boundary

Current work is tracked in Issue #6:
https://github.com/KAFKA2306/kafin3/issues/6

Still unverified and therefore not claimed as complete:

- five years of multiomics trial coverage
- NHGRI sequencing-cost history ingestion
- FDA approval ledger
- modality classification beyond fields explicitly present in official records
- public Web/API deployment

## Security

Local credentials such as `.env`, `token.json`, and `credentials.json` must not be committed. A credential file was previously tracked in Git history; deleting it from the current tree does not revoke the credential or erase historical blobs, so affected credentials must be revoked or rotated separately.
