#!/usr/bin/env python3
"""Validate research claim metadata. This does NOT verify mathematical statements."""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

LEDGER = Path(__file__).resolve().parents[1] / "data" / "claims.json"
STATUSES = {"announced", "source_inspected", "reproduced", "audited", "established", "under_review", "disputed", "refuted", "hypothesis"}
KINDS = {"announcement", "formal_artifact_claim", "proposed_method", "research_hypothesis", "theorem", "obstruction"}
TRACKS = {"alpoge", "masullo", "synthesis", "alternative"}
REQUIRED = {"id", "track", "statement", "status", "kind", "source_urls", "proof_obligation", "verification_note", "as_of"}


def validate_records(document: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return ["top-level JSON must be an object"]
    if document.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    claims = document.get("claims")
    if not isinstance(claims, list) or not claims:
        return errors + ["claims must be a nonempty list"]
    seen: set[str] = set()
    for index, claim in enumerate(claims):
        tag = f"claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{tag}: must be an object")
            continue
        missing = REQUIRED - set(claim)
        if missing:
            errors.append(f"{tag}: missing {sorted(missing)}")
        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not claim_id.strip():
            errors.append(f"{tag}: id must be a nonempty string")
        elif claim_id in seen:
            errors.append(f"{tag}: duplicate id {claim_id}")
        else:
            seen.add(claim_id)
        if claim.get("status") not in STATUSES:
            errors.append(f"{tag}: unknown status")
        if claim.get("kind") not in KINDS:
            errors.append(f"{tag}: unknown kind")
        if claim.get("track") not in TRACKS:
            errors.append(f"{tag}: unknown track")
        for field in ("statement", "proof_obligation", "verification_note"):
            if not isinstance(claim.get(field), str) or not claim[field].strip():
                errors.append(f"{tag}: {field} must be nonempty")
        urls = claim.get("source_urls")
        if not isinstance(urls, list) or not urls or any(not isinstance(url, str) or not url.startswith("https://") for url in urls):
            errors.append(f"{tag}: source_urls must be nonempty HTTPS links")
        try:
            dt.date.fromisoformat(claim.get("as_of", ""))
        except (TypeError, ValueError):
            errors.append(f"{tag}: as_of must be ISO date")
        if claim.get("status") == "established" and claim.get("kind") == "research_hypothesis":
            errors.append(f"{tag}: research_hypothesis cannot be established without reclassification")
    return errors


def main() -> int:
    with LEDGER.open(encoding="utf-8") as stream:
        document = json.load(stream)
    errors = validate_records(document)
    if errors:
        print("\n".join("ERROR: " + error for error in errors), file=sys.stderr)
        return 1
    print(f"Validated {len(document['claims'])} claims; no structural errors. No mathematical proof was checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
