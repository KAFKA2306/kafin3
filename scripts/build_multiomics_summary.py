#!/usr/bin/env python3
"""Build a compact summary from the canonical multiomics domain outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = ROOT / "api" / "v1" / "multiomics"


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build(root: Path) -> dict:
    trials = load(root / "clinical-trials.json")
    costs = load(root / "sequencing-costs.json")
    approvals = load(root / "fda-approvals.json")
    observations = costs.get("observations") or []
    if not observations:
        raise ValueError("sequencing-costs.json has no observations")
    latest_cost = max(observations, key=lambda item: str(item["observation_date"]))

    return {
        "schema_version": 1,
        "retrieved_at": trials["api_version"]["dataTimestamp"],
        "clinical_trials": {
            "coverage_years": trials["coverage_years"],
            "study_count": trials["study_count"],
            "first_study_posted": trials["first_study_posted"],
            "last_study_posted": trials["last_study_posted"],
            "modality_counts": trials["modality_counts"],
        },
        "sequencing_costs": {
            "observation_count": len(observations),
            "first_observation_date": min(
                str(item["observation_date"]) for item in observations
            ),
            "latest": latest_cost,
            "source_url": costs["source_url"],
        },
        "fda_approvals": {
            "coverage_years": approvals["coverage_years"],
            "approval_count": approvals["approval_count"],
            "source_url": approvals["source_url"],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    summary = build(args.root)
    output = args.root / "summary.json"
    output.write_bytes(canonical_json(summary))
    print(
        json.dumps(
            {
                "studies": summary["clinical_trials"]["study_count"],
                "sequencing_cost_observations": summary["sequencing_costs"][
                    "observation_count"
                ],
                "fda_approvals": summary["fda_approvals"]["approval_count"],
            }
        )
    )


if __name__ == "__main__":
    main()
