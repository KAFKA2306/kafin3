"""Verify the canonical multiomics artifact contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


class VerificationError(RuntimeError):
    """Raised when generated multiomics evidence violates the contract."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def verify(root: Path) -> dict[str, int]:
    trials = json.loads((root / "clinical-trials.json").read_text())
    costs = json.loads((root / "sequencing-costs.json").read_text())
    approvals = json.loads((root / "fda-approvals.json").read_text())
    summary = json.loads((root / "summary.json").read_text())
    manifest = json.loads((root / "manifest.json").read_text())

    _require(trials["coverage_years"] == 5, "clinical-trials coverage_years must be 5")
    _require(trials["study_count"] > 0, "clinical-trials must contain studies")
    _require(bool(trials["api_version"].get("dataTimestamp")), "dataTimestamp is required")
    _require(len(costs["observations"]) >= 10, "sequencing-costs needs at least 10 observations")
    _require(
        costs["observations"][0]["observation_date"] <= "2021-01-01",
        "sequencing-cost history is too short",
    )
    _require(approvals["approval_count"] > 0, "fda-approvals must contain approvals")
    _require(
        all(row["source_url"].startswith("https://www.accessdata.fda.gov/") for row in approvals["approvals"]),
        "FDA approval rows must point to accessdata.fda.gov",
    )
    _require(
        all(row["omics_modalities"] == ["unknown"] for row in approvals["approvals"]),
        "FDA approval modalities must remain unknown until evidence supports classification",
    )
    _require(
        set(manifest["sources"]) == {"clinical_trials_version", "nhgri", "drugs_at_fda"},
        "manifest source set changed",
    )
    _require(
        summary["clinical_trials"]["study_count"] == trials["study_count"],
        "summary clinical trial count does not match ledger",
    )
    _require(
        summary["sequencing_costs"]["observation_count"] == len(costs["observations"]),
        "summary sequencing cost count does not match ledger",
    )
    _require(
        summary["fda_approvals"]["approval_count"] == approvals["approval_count"],
        "summary FDA approval count does not match ledger",
    )
    _require("studies" not in summary["clinical_trials"], "summary must not copy clinical trial rows")
    _require("approvals" not in summary["fda_approvals"], "summary must not copy FDA approval rows")

    return {
        "trials": trials["study_count"],
        "sequencing_cost_observations": len(costs["observations"]),
        "fda_approvals": approvals["approval_count"],
        "summary_bytes": (root / "summary.json").stat().st_size,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default="api/v1/multiomics", type=Path)
    args = parser.parse_args()
    print(verify(args.root))


if __name__ == "__main__":
    main()
