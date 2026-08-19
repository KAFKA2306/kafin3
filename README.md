# kafin3 — multiomics evidence

[![CI](https://github.com/KAFKA2306/kafin3/actions/workflows/ci.yml/badge.svg)](https://github.com/KAFKA2306/kafin3/actions/workflows/ci.yml)
[![Multiomics source](https://github.com/KAFKA2306/kafin3/actions/workflows/multiomics-source.yml/badge.svg)](https://github.com/KAFKA2306/kafin3/actions/workflows/multiomics-source.yml)

`kafin3` is an evidence-first multiomics dataset. Legacy finance, Streamlit, FastAPI, and LLM prototypes are not supported interfaces.

## Canonical outputs

`api/v1/multiomics/` is the current machine-readable surface:

- `clinical-trials.json` — ClinicalTrials.gov API v2 studies, five-year coverage window, phase/status/sponsor/timing and explicit omics evidence
- `sequencing-costs.json` — NHGRI cost per megabase and cost per genome history
- `fda-approvals.json` — approved Drugs@FDA submissions with application/product identity and official reverse links
- `index.json` — dataset entry points
- `manifest.json` — source URLs, hashes and generated-file hashes

Rebuild from the primary sources:

```bash
python -m pip install xlrd==2.0.2
python scripts/update_multiomics.py
```

## Data contract

- ClinicalTrials.gov `/api/v2/version` metadata, including `dataTimestamp`, is preserved.
- Trial modality is assigned only when the official study record explicitly contains genomics/transcriptomics/proteomics/multiomics wording; otherwise it remains `unknown`.
- Study start, primary completion, completion, first-posted, and last-update dates remain separate events.
- NHGRI methodology is retained with its sequencing-cost observations; methodology changes are not silently normalized away.
- Drugs@FDA approvals point back to their official application page. FDA records are not assigned an omics modality from product names or sponsor marketing; absent explicit evidence, modality remains `unknown`.
- Source URL, retrieval metadata and SHA-256 provenance are retained so every aggregate can be traced back to the source dataset.

## Primary sources

- ClinicalTrials.gov API v2: https://clinicaltrials.gov/data-api/api
- NHGRI DNA Sequencing Costs: https://www.genome.gov/about-genomics/fact-sheets/DNA-Sequencing-Costs-Data
- Drugs@FDA Data Files: https://www.fda.gov/drugs/drug-approvals-and-databases/drugsfda-data-files

## Verification

```bash
python -m unittest discover -s tests -v
```

CI additionally downloads all three live primary sources and fails closed when the source schema, five-year trial coverage, sequencing-cost history, or FDA approval ledger is missing.

Tracked work: https://github.com/KAFKA2306/kafin3/issues/6
