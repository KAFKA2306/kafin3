#!/usr/bin/env python3
"""Collect multiomics-related interventional studies from ClinicalTrials.gov API v2."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://clinicaltrials.gov/api/v2"
DEFAULT_QUERY = "genomics OR transcriptomics OR proteomics OR multiomics"


def get_json(path: str, params: dict[str, object] | None = None) -> tuple[dict[str, object], bytes, str]:
    query = f"?{urlencode(params)}" if params else ""
    url = f"{API}{path}{query}"
    req = Request(url, headers={"User-Agent": "multiomics/1.0 github.com/KAFKA2306/kafin3"})
    with urlopen(req, timeout=60) as response:
        raw = response.read()
    return json.loads(raw), raw, url


def date_value(module: dict[str, object], key: str) -> str | None:
    value = module.get(key)
    return value.get("date") if isinstance(value, dict) else None


def normalize(study: dict[str, object]) -> dict[str, object]:
    protocol = study.get("protocolSection", {})
    identification = protocol.get("identificationModule", {})
    status = protocol.get("statusModule", {})
    design = protocol.get("designModule", {})
    sponsors = protocol.get("sponsorCollaboratorsModule", {})
    conditions = protocol.get("conditionsModule", {})
    arms = protocol.get("armsInterventionsModule", {})
    interventions = arms.get("interventions") or []
    lead = sponsors.get("leadSponsor") or {}
    enrollment = design.get("enrollmentInfo") or {}

    return {
        "nct_id": identification.get("nctId"),
        "title": identification.get("briefTitle"),
        "study_type": design.get("studyType"),
        "phases": design.get("phases") or [],
        "status": status.get("overallStatus"),
        "start_date": date_value(status, "startDateStruct"),
        "primary_completion_date": date_value(status, "primaryCompletionDateStruct"),
        "completion_date": date_value(status, "completionDateStruct"),
        "last_update_posted": date_value(status, "studyFirstPostDateStruct") if False else date_value(status, "lastUpdatePostDateStruct"),
        "lead_sponsor": lead.get("name"),
        "sponsor_class": lead.get("class"),
        "enrollment": enrollment.get("count"),
        "enrollment_type": enrollment.get("type"),
        "conditions": conditions.get("conditions") or [],
        "interventions": [
            {
                "type": item.get("type"),
                "name": item.get("name"),
            }
            for item in interventions
        ],
    }


def collect(query: str, pages: int, page_size: int) -> dict[str, object]:
    version, version_raw, version_url = get_json("/version")
    page_token: str | None = None
    studies: list[dict[str, object]] = []
    source_pages: list[dict[str, object]] = []

    for _ in range(pages):
        params: dict[str, object] = {
            "query.term": query,
            "filter.overallStatus": "RECRUITING|NOT_YET_RECRUITING|ACTIVE_NOT_RECRUITING|COMPLETED|TERMINATED|WITHDRAWN|SUSPENDED|ENROLLING_BY_INVITATION",
            "pageSize": page_size,
            "format": "json",
        }
        if page_token:
            params["pageToken"] = page_token
        payload, raw, url = get_json("/studies", params)
        page_studies = payload.get("studies") or []
        studies.extend(normalize(study) for study in page_studies)
        source_pages.append({"url": url, "sha256": hashlib.sha256(raw).hexdigest(), "count": len(page_studies)})
        page_token = payload.get("nextPageToken")
        if not page_token:
            break

    return {
        "schema_version": 1,
        "publisher": "ClinicalTrials.gov / U.S. National Library of Medicine",
        "query": query,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "api_version": version,
        "version_source": {"url": version_url, "sha256": hashlib.sha256(version_raw).hexdigest()},
        "source_pages": source_pages,
        "studies": studies,
        "next_page_token": page_token,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--pages", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--output", type=Path, default=Path("data/multiomics/clinical-trials.json"))
    args = parser.parse_args()
    payload = collect(args.query, args.pages, args.page_size)
    if not payload["studies"]:
        raise SystemExit("ClinicalTrials.gov returned no matching studies")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(payload['studies'])} studies -> {args.output}")


if __name__ == "__main__":
    main()
