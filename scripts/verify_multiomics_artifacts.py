#!/usr/bin/env python3
"""Validate canonical multiomics artifacts with one shared contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(root: Path, name: str) -> dict:
    return json.loads((root / name).read_text(encoding="utf-8"))


def verify(root: Path) -> None:
    trials = load(root, "clinical-trials.json")
    costs = load(root, "sequencing-costs.json")
    approvals = load(root, "fda-approvals.json")
    summary = load(root, "summary.json")
    manifest = load(root, "manifest.json")

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
    assert set(manifest["sources"]) == {
        "clinical_trials_version",
        "nhgri",
        "drugs_at_fda",
    }
    assert summary["clinical_trials"]["study_count"] == trials["study_count"]
    assert summary["sequencing_costs"]["observation_count"] == len(costs["observations"])
    assert summary["fda_approvals"]["approval_count"] == approvals["approval_count"]
    assert "studies" not in summary["clinical_trials"]
    assert "approvals" not in summary["fda_approvals"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    verify(args.root)
    print(f"verified canonical multiomics artifacts: {args.root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
