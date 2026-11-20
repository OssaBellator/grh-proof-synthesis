"""Offline checks for the pinned arithmetic source receipt."""

from copy import deepcopy
import hashlib
from io import BytesIO, StringIO
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from urllib.parse import unquote, urlsplit

from tools import check_arithmetic_handoff as audit


class ArithmeticHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads(audit.RECEIPT.read_text(encoding="utf-8"))

    def test_receipt_schema_and_reproducibility(self):
        self.assertEqual(self.registry, audit.build_registry())
        audit.validate_registry(self.registry)
        self.assertEqual(self.registry["schema_version"], 1)
        self.assertEqual(
            self.registry["revision"], "0fb9869c6e6d7b54b67de803af0e0be29d37fc22"
        )

    def test_pinned_allowlist_and_budgets(self):
        sources = self.registry["sources"]
        self.assertLessEqual(sum(source["bytes"] + 1 for source in sources), audit.MAX_TOTAL_BYTES)
        for source in sources:
            with self.subTest(source=source["id"]):
                self.assertRegex(source["sha256"], r"^[0-9a-f]{64}$")
                self.assertLessEqual(1, source["bytes"])
                self.assertLessEqual(source["bytes"], audit.MAX_FILE_BYTES)
                self.assertRegex(source["path"], r"^src/(?:[^/]+/)*[^/]+\.lean$")
                self.assertNotIn("..", source["path"].split("/"))
                url = urlsplit(source["raw_url"])
                self.assertEqual((url.scheme, url.netloc), ("https", "raw.githubusercontent.com"))
                self.assertEqual((url.query, url.fragment), ("", ""))
                self.assertEqual(
                    unquote(url.path),
                    f"/CocoSgt/riemann-hypothesis-lean/{audit.REVISION}/{source['path']}",
                )

    def test_all_handoff_arguments_and_distinct_projections(self):
        edges = self.registry["edges"]
        self.assertEqual({
            (edge["detail"], edge["to"]) for edge in edges
            if edge["from"] == "literature-call" and edge["relation"] == "supplies"
            and edge["detail"] in {"P", "F", "hA", "hM", "hX", "hL"}
        }, {
            ("P", "eigen-bundle"), ("F", "local-bundle"), ("hA", "theta-first"),
            ("hM", "theta-second"), ("hX", "covol"), ("hL", "ll-literature"),
        })
        triples = {(edge["from"], edge["relation"], edge["to"]) for edge in edges}
        self.assertIn(("literature-call", "forwarded", "vwin"), triples)
        self.assertIn(("theta-first", "projects", "theta-pair"), triples)
        self.assertIn(("theta-second", "projects", "theta-pair"), triples)
        self.assertIn(("theta-first", "type", "theta-agree"), triples)
        self.assertIn(("theta-second", "type", "local-match"), triples)
        self.assertIn(("ll-adapter", "forwarded", "ll-type"), triples)
        self.assertIn(("row-wrapper", "supplies", "ll-witness"), triples)

    def test_unknown_node_source_and_changed_pin_are_rejected(self):
        changes = (
            ("edges", "to", "missing-node", "Unknown edge endpoint"),
            ("nodes", "evidence", {"source_id": "missing-source"}, "Unknown source"),
            ("sources", "sha256", "0" * 64, "differ from the fixed allowlist"),
        )
        for collection, key, value, error in changes:
            with self.subTest(key=key):
                broken = deepcopy(self.registry)
                broken[collection][0][key] = value
                with self.assertRaisesRegex(ValueError, error):
                    audit.validate_registry(broken)

    def test_inferred_edge_cannot_be_promoted(self):
        broken = deepcopy(self.registry)
        inferred = next(edge for edge in broken["edges"] if edge["status"] == "inferred")
        self.assertNotIn("evidence", inferred)
        target = next(node for node in broken["nodes"] if node["id"] == inferred["to"])
        self.assertEqual(target["status"], "hypothetical")
        inferred.update(status="source-backed", relation="calls", evidence=broken["edges"][0]["evidence"])
        with self.assertRaisesRegex(ValueError, "touches a hypothetical node"):
            audit.validate_registry(broken)

    def test_invalid_line_range_is_rejected(self):
        broken = deepcopy(self.registry)
        broken["nodes"][0]["evidence"]["lines"] = [10, 9]
        with self.assertRaisesRegex(ValueError, "Invalid source line range"):
            audit.validate_registry(broken)

    def test_byte_length_and_hash_are_both_enforced(self):
        body = b"theorem example : True := trivial\n"
        source = {
            "id": "fixture", "path": "src/example.lean", "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(), "raw_url": audit.RAW + "src/example.lean",
        }
        with patch.object(audit, "build_opener") as opener, redirect_stdout(StringIO()):
            response = opener.return_value.open
            response.return_value = BytesIO(body)
            self.assertEqual(audit.fetch_sources([source]), {"fixture": [body.decode().strip()]})
            for invalid in (b"X" * len(body), body[:-1], body + b"X"):
                response.return_value = BytesIO(invalid)
                with self.assertRaisesRegex(ValueError, "Byte length or SHA-256 mismatch"):
                    audit.fetch_sources([source])

    def test_source_anchor_is_checked_at_reported_lines(self):
        node = self.registry["nodes"][0]
        first, _ = node["evidence"]["lines"]
        lines = [""] * first
        lines[first - 2] = node["evidence"]["anchor"]
        with self.assertRaisesRegex(ValueError, "Missing anchor"):
            audit.check_anchors({"nodes": [node], "edges": []}, {"main": lines})


if __name__ == "__main__":
    unittest.main()
