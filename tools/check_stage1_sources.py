"""Verify the fixed Task 05 source selection and the local extraction signature."""

import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from urllib.request import HTTPRedirectHandler, build_opener


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "stage1-sources.json"
CACHE = ROOT / ".source-tmp" / "task-05"
EXTRACTION = ROOT / "lean" / "extraction" / "Extraction" / "Stage1Primitive.lean"
MIRROR = "CocoSgt/riemann-hypothesis-lean"
REVISION = "0fb9869c6e6d7b54b67de803af0e0be29d37fc22"
MAX_BYTES = 300 * 1024
RAW_BASE = f"https://raw.githubusercontent.com/{MIRROR}/{REVISION}/"


class RejectRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def validate_registry(registry):
    if (registry["schema_version"], registry["mirror"], registry["revision"], registry["evidence"]) != (
        1, MIRROR, REVISION, "source_inspected"
    ):
        raise ValueError("unexpected registry identity or evidence status")
    sources = registry["sources"]
    if not 10 <= len(sources) <= 18:
        raise ValueError("expected 10 to 18 source files")
    filenames = set()
    total = 0
    for source in sources:
        path = source["path"]
        name = PurePosixPath(path).name
        if not re.fullmatch(r"src/(?:[A-Za-z0-9_]+/)+[A-Za-z0-9_]+\.lean", path) or name in filenames:
            raise ValueError(f"invalid or duplicate source path: {path}")
        filenames.add(name)
        size = source["bytes"]
        if type(size) is not int or size < 1 or not re.fullmatch(r"[0-9a-f]{64}", source["sha256"]):
            raise ValueError(f"invalid source identity: {path}")
        total += size
        if not source["anchors"]:
            raise ValueError(f"missing declaration anchors: {path}")
        anchors = set()
        for anchor in source["anchors"]:
            start, end = anchor["lines"]
            if (not 1 <= start <= end or not anchor["text"].strip()
                    or len(anchor["text"].splitlines()) != end - start + 1 or anchor["name"] in anchors):
                raise ValueError(f"invalid declaration anchor: {path} {anchor['name']}")
            anchors.add(anchor["name"])
    if total > MAX_BYTES:
        raise ValueError("source budget exceeded")
    return sources


def check_source(source, data):
    path = source["path"]
    if len(data) != source["bytes"] or hashlib.sha256(data).hexdigest() != source["sha256"]:
        raise ValueError(f"source identity mismatch: {path}")
    lines = data.decode("utf-8").splitlines()
    for anchor in source["anchors"]:
        start, end = anchor["lines"]
        if "\n".join(lines[start - 1:end]) != anchor["text"]:
            raise ValueError(f"source anchor mismatch: {path}:{start}-{end} {anchor['name']}")


def check_extraction(sources, local_text):
    source = next(s for s in sources if s["path"].endswith("/Stage1Succ.lean"))
    anchor = next(a for a in source["anchors"] if a["name"] == "stage1_prim")
    expected = anchor["text"].removeprefix("private ")
    if f"\n{expected}\n" not in local_text:
        raise ValueError("local stage1_prim signature differs from the pinned declaration")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="read only from the repository cache")
    args = parser.parse_args()
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    sources = validate_registry(registry)
    check_extraction(sources, EXTRACTION.read_text(encoding="utf-8"))
    if not args.offline:
        CACHE.mkdir(parents=True, exist_ok=True)
    opener = build_opener(RejectRedirect())
    for source in sources:
        path = source["path"]
        cached = CACHE / PurePosixPath(path).name
        if args.offline:
            stream = cached.open("rb")
        else:
            stream = opener.open(RAW_BASE + path, timeout=20)
        with stream:
            data = stream.read(source["bytes"] + 1)
        check_source(source, data)
        if not args.offline:
            cached.write_bytes(data)
        print(f"{source['sha256']}  {path}  ({len(data)} bytes)")
    total = sum(s["bytes"] for s in sources)
    print(f"Matched {len(sources)} files ({total} bytes), source anchors, and local stage1_prim signature.")
    print("Evidence level: source inspection. This command performs no Lean build or analytic proof check.")


if __name__ == "__main__":
    main()
