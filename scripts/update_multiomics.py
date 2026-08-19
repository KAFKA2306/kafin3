#!/usr/bin/env python3
"""Build the canonical multiomics dataset from NIH and FDA primary sources."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import urllib.request
import zipfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from collect_clinical_trials import DEFAULT_QUERY, collect

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "api" / "v1" / "multiomics"
NHGRI_URL = "https://www.genome.gov/sites/default/files/media/files/2023-05/Sequencing_Cost_Data_Table_May2022.xls"
NHGRI_PAGE = "https://www.genome.gov/about-genomics/fact-sheets/DNA-Sequencing-Costs-Data"
FDA_URL = "https://www.fda.gov/media/89850/download?attachment="
FDA_PAGE = "https://www.fda.gov/drugs/drug-approvals-and-databases/drugsfda-data-files"
UA = "multiomics/1.0 github.com/KAFKA2306/kafin3"


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def parse_date(value: object) -> str | None:
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%Y%m%d", "%m/%d/%Y", "%m/%d/%y", "%Y-%m", "%b-%y", "%b %Y", "%Y"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            pass
    return None


def normalize_header(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).strip()


def parse_nhgri_xls(raw: bytes) -> list[dict[str, object]]:
    try:
        import xlrd  # type: ignore
    except ImportError as exc:
        raise RuntimeError("xlrd is required to read the NHGRI .xls workbook") from exc
    book = xlrd.open_workbook(file_contents=raw)
    for sheet in book.sheets():
        header_row = None
        date_col = mb_col = genome_col = None
        for r in range(min(sheet.nrows, 30)):
            headers = [normalize_header(sheet.cell_value(r, c)) for c in range(sheet.ncols)]
            for c, header in enumerate(headers):
                if header in {"date", "month year", "time"} or "date" in header:
                    date_col = c
                if "cost per mb" in header or "cost per megabase" in header:
                    mb_col = c
                if "cost per genome" in header:
                    genome_col = c
            if date_col is not None and mb_col is not None and genome_col is not None:
                header_row = r
                break
        if header_row is None:
            continue
        rows: list[dict[str, object]] = []
        for r in range(header_row + 1, sheet.nrows):
            raw_date = sheet.cell_value(r, date_col)
            if sheet.cell_type(r, date_col) == xlrd.XL_CELL_DATE:
                observed = xlrd.xldate_as_datetime(raw_date, book.datemode).date().isoformat()
            else:
                observed = parse_date(raw_date)
            if not observed:
                continue
            try:
                per_mb = float(sheet.cell_value(r, mb_col))
                per_genome = float(sheet.cell_value(r, genome_col))
            except (TypeError, ValueError):
                continue
            rows.append({
                "observation_date": observed,
                "cost_per_megabase_usd": per_mb,
                "cost_per_genome_usd": per_genome,
                "methodology": "NHGRI Genome Sequencing Program production-oriented sequencing cost accounting",
            })
        if rows:
            return sorted(rows, key=lambda row: str(row["observation_date"]))
    raise ValueError("NHGRI workbook did not contain date/cost-per-Mb/cost-per-genome columns")


def decode_table(data: bytes) -> str:
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError("unable to decode Drugs@FDA table")


def zip_table(archive: zipfile.ZipFile, wanted: str) -> list[dict[str, str]]:
    candidates = [name for name in archive.namelist() if Path(name).name.lower() == wanted.lower()]
    if not candidates:
        raise ValueError(f"Drugs@FDA archive missing {wanted}; files={archive.namelist()}")
    return list(csv.DictReader(io.StringIO(decode_table(archive.read(candidates[0]))), delimiter="\t"))


def parse_fda_zip(raw: bytes, years: int = 5) -> list[dict[str, object]]:
    cutoff = date.today() - timedelta(days=366 * years)
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        applications = {row.get("ApplNo", "").strip(): row for row in zip_table(archive, "Applications.txt")}
        products_by_app: dict[str, list[dict[str, str]]] = {}
        for row in zip_table(archive, "Products.txt"):
            products_by_app.setdefault(row.get("ApplNo", "").strip(), []).append(row)
        submissions = zip_table(archive, "Submissions.txt")
    approvals: list[dict[str, object]] = []
    for row in submissions:
        if row.get("SubmissionStatus", "").strip().upper() != "AP":
            continue
        approval_date = parse_date(row.get("SubmissionStatusDate"))
        if not approval_date or date.fromisoformat(approval_date) < cutoff:
            continue
        appl_no = row.get("ApplNo", "").strip()
        app = applications.get(appl_no, {})
        products = products_by_app.get(appl_no, [])
        approvals.append({
            "application_number": appl_no,
            "application_type": app.get("ApplType") or None,
            "sponsor": app.get("SponsorName") or None,
            "submission_type": row.get("SubmissionType") or None,
            "submission_number": row.get("SubmissionNo") or None,
            "approval_date": approval_date,
            "review_priority": row.get("ReviewPriority") or None,
            "products": [{
                "product_number": product.get("ProductNo") or None,
                "drug_name": product.get("DrugName") or None,
                "active_ingredient": product.get("ActiveIngredient") or None,
                "form": product.get("Form") or None,
                "strength": product.get("Strength") or None,
            } for product in products],
            "omics_modalities": ["unknown"],
            "modality_evidence": [],
            "source_url": f"https://www.accessdata.fda.gov/scripts/cder/daf/index.cfm?event=overview.process&ApplNo={appl_no}",
        })
    return sorted(approvals, key=lambda row: (str(row["approval_date"]), str(row["application_number"])))


def trial_coverage(studies: list[dict[str, object]], years: int) -> dict[str, object]:
    cutoff = date.today() - timedelta(days=366 * years)
    eligible = []
    for study in studies:
        first = parse_date(study.get("study_first_posted"))
        if first and date.fromisoformat(first) >= cutoff:
            eligible.append(study)
    if not eligible:
        raise ValueError("ClinicalTrials.gov returned no studies in the requested coverage window")
    dates = sorted(str(study["study_first_posted"]) for study in eligible if study.get("study_first_posted"))
    modalities: dict[str, int] = {}
    for study in eligible:
        for modality in study.get("omics_modalities") or ["unknown"]:
            modalities[str(modality)] = modalities.get(str(modality), 0) + 1
    return {
        "schema_version": 1,
        "coverage_years": years,
        "cutoff_date": cutoff.isoformat(),
        "study_count": len(eligible),
        "first_study_posted": dates[0],
        "last_study_posted": dates[-1],
        "modality_counts": dict(sorted(modalities.items())),
        "studies": eligible,
    }


def build(years: int, trial_pages: int, trial_page_size: int) -> dict[str, object]:
    trials = collect(DEFAULT_QUERY, trial_pages, trial_page_size)
    if trials.get("next_page_token"):
        raise ValueError("ClinicalTrials.gov pagination was truncated; increase --trial-pages")
    trial_view = trial_coverage(trials["studies"], years)
    nhgri_raw = fetch(NHGRI_URL)
    sequencing_costs = parse_nhgri_xls(nhgri_raw)
    if len(sequencing_costs) < 10:
        raise ValueError("NHGRI sequencing-cost history is unexpectedly short")
    fda_raw = fetch(FDA_URL)
    approvals = parse_fda_zip(fda_raw, years=years)
    if not approvals:
        raise ValueError("Drugs@FDA returned no approved submissions in coverage window")
    retrieved_at = datetime.now(timezone.utc).isoformat()
    return {
        "retrieved_at": retrieved_at,
        "clinical_trials": {**trial_view, "api_version": trials["api_version"], "query": trials["query"], "source_pages": trials["source_pages"], "version_source": trials["version_source"]},
        "sequencing_costs": {"schema_version": 1, "publisher": "National Human Genome Research Institute", "source_url": NHGRI_URL, "source_page": NHGRI_PAGE, "source_sha256": sha256(nhgri_raw), "observations": sequencing_costs},
        "fda_approvals": {"schema_version": 1, "publisher": "U.S. Food and Drug Administration / Drugs@FDA", "source_url": FDA_URL, "source_page": FDA_PAGE, "source_sha256": sha256(fda_raw), "coverage_years": years, "approval_count": len(approvals), "approvals": approvals},
    }


def write(output: Path, payload: dict[str, object]) -> None:
    output.mkdir(parents=True, exist_ok=True)
    files = {"clinical-trials.json": payload["clinical_trials"], "sequencing-costs.json": payload["sequencing_costs"], "fda-approvals.json": payload["fda_approvals"]}
    for name, value in files.items():
        (output / name).write_bytes(canonical_json(value))
    index = {"schema_version": 1, "retrieved_at": payload["retrieved_at"], "datasets": {"clinical_trials": "clinical-trials.json", "sequencing_costs": "sequencing-costs.json", "fda_approvals": "fda-approvals.json"}}
    (output / "index.json").write_bytes(canonical_json(index))
    manifest = {
        "schema_version": 1,
        "retrieved_at": payload["retrieved_at"],
        "sources": {
            "clinical_trials_version": payload["clinical_trials"]["version_source"],
            "nhgri": {"url": NHGRI_URL, "sha256": payload["sequencing_costs"]["source_sha256"]},
            "drugs_at_fda": {"url": FDA_URL, "sha256": payload["fda_approvals"]["source_sha256"]},
        },
        "files": {name: {"sha256": sha256((output / name).read_bytes()), "bytes": (output / name).stat().st_size} for name in sorted([*files, "index.json"])},
    }
    (output / "manifest.json").write_bytes(canonical_json(manifest))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--years", type=int, default=5)
    parser.add_argument("--trial-pages", type=int, default=25)
    parser.add_argument("--trial-page-size", type=int, default=1000)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    payload = build(args.years, args.trial_pages, args.trial_page_size)
    write(args.output, payload)
    print(json.dumps({"trials": payload["clinical_trials"]["study_count"], "sequencing_cost_observations": len(payload["sequencing_costs"]["observations"]), "fda_approvals": payload["fda_approvals"]["approval_count"]}))


if __name__ == "__main__":
    main()
