#!/usr/bin/env python3
"""Verify canonical multiomics artifacts with one shared correctness contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def verify(root: Path) -> dict[str, int]:
    trials = json.loads((root / "clinical-trials.json").read_text())
    costs = json.loads((root / "sequencing-costs.json").read_text())
    approvals = json.loads((root / "fda-approvals.json").read_text())
    summary = json.loads((root / "summary.json").read_text())
    manifest = json.loads((root / "manifest.json").read_text())

    assert trials["coverage_years"] == 5
    assert trials["study_count"] > 0
    assert trials["api_version"].get("dataTimestamp")
    assert len(costs["observations"]) >= 10
    assert costs["observations"][0]["observation_date"] <= "2021-01-01"
    assert approvals["approval_count"] > 0
    assert all(
        row["source_url"].startswith("https://www.accessdata.fda.gov/")
        for row in approvals["approvals"]
    )
    assert all(row["omics_modalities"] == ["unknown"] for row in approvals["approvals"])
    assert set(manifest["sources"]) == {"clinical_trials_version", "nhgri", "drugs_at_fda"}
    assert summary["clinical_trials"]["study_count"] == trials["study_count"]
    assert summary["sequencing_costs"]["observation_count"] == len(costs["observations"])
    assert summary["fda_approvals"]["approval_count"] == approvals["approval_count"]
    assert "studies" not in summary["clinical_trials"]
    assert "approvals" not in summary["fda_approvals"]

    return {
        "trials": trials["study_count"],
        "sequencing_cost_observations": len(costs["observations"]),
        "fda_approvals": approvals["approval_count"],
        "summary_bytes": (root / "summary.json").stat().st_size,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("api/v1/multiomics"))
    args = parser.parse_args()
    print(verify(args.root))


if __name__ == "__main__":
    main()
