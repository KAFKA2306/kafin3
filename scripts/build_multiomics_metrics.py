#!/usr/bin/env python3
"""Build compact decision metrics from canonical Multiomics summary evidence."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "api" / "v1" / "multiomics"
DEFAULT_OUTPUT = DEFAULT_INPUT / "metrics.json"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def date_part(value: str) -> str:
    return value.split("T", 1)[0]


def build(input_dir: Path) -> dict:
    summary = load(input_dir / "summary.json")
    manifest = load(input_dir / "manifest.json")
    sources = manifest["sources"]
    retrieved = date_part(str(summary["retrieved_at"]))
    trials = summary["clinical_trials"]
    approvals = summary["fda_approvals"]
    sequencing = summary["sequencing_costs"]
    latest = sequencing["latest"]

    observations = [
        {
            "metric": "clinical_trial_count",
            "as_of": retrieved,
            "value": trials["study_count"],
            "unit": "studies",
            "provider": "ClinicalTrials.gov",
            "product": "Multiomics-related trial ledger",
            "geography": "global registry",
            "period": f"{trials['coverage_years']}-year coverage",
            "qualifier": "registered studies; trial registration is not a trial result or approval",
            "source_url": sources["clinical_trials_version"]["url"],
        },
        {
            "metric": "multiomics_trial_count",
            "as_of": retrieved,
            "value": trials["modality_counts"]["multiomics"],
            "unit": "studies",
            "provider": "ClinicalTrials.gov",
            "product": "Explicit multiomics modality records",
            "geography": "global registry",
            "period": f"{trials['coverage_years']}-year coverage",
            "qualifier": "only explicitly classified modality records; unknown is not inferred",
            "source_url": sources["clinical_trials_version"]["url"],
        },
        {
            "metric": "fda_approval_count",
            "as_of": retrieved,
            "value": approvals["approval_count"],
            "unit": "approval records",
            "provider": "U.S. Food and Drug Administration",
            "product": "Drugs@FDA approval ledger",
            "geography": "United States",
            "period": f"{approvals['coverage_years']}-year coverage",
            "qualifier": "official approval records; not company press-release claims",
            "source_url": sources["drugs_at_fda"]["url"],
        },
        {
            "metric": "sequencing_cost_per_genome_usd",
            "as_of": latest["observation_date"],
            "value": latest["cost_per_genome_usd"],
            "unit": "USD/genome",
            "provider": "National Human Genome Research Institute",
            "product": "DNA sequencing cost history",
            "geography": "program-level benchmark",
            "period": "observation date",
            "qualifier": latest["methodology"],
            "source_url": sources["nhgri"]["url"],
        },
        {
            "metric": "sequencing_cost_per_megabase_usd",
            "as_of": latest["observation_date"],
            "value": latest["cost_per_megabase_usd"],
            "unit": "USD/megabase",
            "provider": "National Human Genome Research Institute",
            "product": "DNA sequencing cost history",
            "geography": "program-level benchmark",
            "period": "observation date",
            "qualifier": latest["methodology"],
            "source_url": sources["nhgri"]["url"],
        },
    ]
    return {"schema_version": 1, "observations": observations}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    payload = build(args.input_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
