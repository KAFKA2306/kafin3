"""Canonical multiomics artifact verification shared by CI and source refresh."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


EXPECTED_SOURCES = {"clinical_trials_version", "nhgri", "drugs_at_fda"}


def _read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{path}: expected JSON object")
    return value


def verify_multiomics_root(root: Path) -> dict[str, int]:
    trials = _read_json(root / "clinical-trials.json")
    costs = _read_json(root / "sequencing-costs.json")
    approvals = _read_json(root / "fda-approvals.json")
    summary = _read_json(root / "summary.json")
    manifest = _read_json(root / "manifest.json")

    assert trials["coverage_years"] == 5
    assert trials["study_count"] > 0
    assert trials["api_version"].get("dataTimestamp")

    observations = costs["observations"]
    assert len(observations) >= 10
    assert observations[0]["observation_date"] <= "2021-01-01"

    approval_rows = approvals["approvals"]
    assert approvals["approval_count"] > 0
    assert all(
        row["source_url"].startswith("https://www.accessdata.fda.gov/")
        for row in approval_rows
    )
    assert all(row["omics_modalities"] == ["unknown"] for row in approval_rows)

    assert set(manifest["sources"]) == EXPECTED_SOURCES
    assert summary["clinical_trials"]["study_count"] == trials["study_count"]
    assert summary["sequencing_costs"]["observation_count"] == len(observations)
    assert summary["fda_approvals"]["approval_count"] == approvals["approval_count"]
    assert "studies" not in summary["clinical_trials"]
    assert "approvals" not in summary["fda_approvals"]

    return {
        "trials": trials["study_count"],
        "sequencing_cost_observations": len(observations),
        "fda_approvals": approvals["approval_count"],
        "summary_bytes": (root / "summary.json").stat().st_size,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("api/v1/multiomics"))
    args = parser.parse_args()
    print(verify_multiomics_root(args.root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
