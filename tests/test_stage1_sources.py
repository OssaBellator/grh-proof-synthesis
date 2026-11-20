import copy
import hashlib
import json
import unittest

from tools import check_stage1_sources as checker


class Stage1SourcesTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads(checker.REGISTRY.read_text(encoding="utf-8"))

    def test_pinned_declarations(self):
        sources = checker.validate_registry(self.registry)
        anchors = {a["name"]: a["text"] for source in sources for a in source["anchors"]}
        self.assertEqual(len(sources), 18)
        self.assertEqual(sum(s["bytes"] for s in sources), 134978)
        self.assertTrue(anchors["stage1"].startswith("theorem stage1 :\n    ∃ C : ℝ, 0 < C ∧ ∀"))
        self.assertIn("0 < N₀ → ∃ Y₀ : ℝ, ∀ Y ≥ Y₀", anchors["stage1"])
        self.assertIn("meanSqK", anchors["stage input applications"])
        self.assertIn("pnt_progressions_relative_weak_holds", anchors["stage input applications"])
        self.assertIn("∀ y ∈ A, ∀ κ : ℕ → ℂ", anchors["MeanSq"])
        self.assertIn("q % m₀ = a₀ % m₀ ∧ X ^ (1 / 2 : ℝ) < (q : ℝ)", anchors["PPset"])
        checker.check_extraction(sources, checker.EXTRACTION.read_text(encoding="utf-8"))

    def test_finite_source_budget_and_evidence_level(self):
        for change, message in (
            ({"evidence": "reproduced"}, "evidence status"),
            ({"sources": self.registry["sources"] * 2}, "10 to 18"),
        ):
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                checker.validate_registry(dict(self.registry, **change))
        oversized = copy.deepcopy(self.registry)
        oversized["sources"][0]["bytes"] = checker.MAX_BYTES
        with self.assertRaisesRegex(ValueError, "budget"):
            checker.validate_registry(oversized)
        invalid_path = copy.deepcopy(self.registry)
        invalid_path["sources"][0]["path"] = "src/../Example.lean"
        with self.assertRaisesRegex(ValueError, "path"):
            checker.validate_registry(invalid_path)

    def test_reader_checks_size_digest_and_anchor(self):
        data = b"-- header\r\ntheorem example : True := by trivial\r\n"
        source = {
            "path": "src/Test/Example.lean",
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "anchors": [{"name": "example", "lines": [2, 2], "text": "theorem example : True := by trivial"}],
        }
        checker.check_source(source, data)
        for changed in (data + b"x", data.replace(b"True", b"true")):
            with self.subTest(data=changed), self.assertRaisesRegex(ValueError, "source identity mismatch"):
                checker.check_source(source, changed)
        with self.assertRaisesRegex(ValueError, "source anchor mismatch"):
            checker.check_source(dict(source, anchors=[dict(source["anchors"][0], lines=[1, 1])]), data)

    def test_scale_dependent_constant_fails_signature_check(self):
        # Even a repinned hash must agree with the expected declaration text.
        anchor = next(a for a in self.registry["sources"][0]["anchors"] if a["name"] == "stage1")
        weakened = anchor["text"].replace("∃ C : ℝ, 0 < C ∧ ∀", "∀", 1).replace(
            "∀ Y ≥ Y₀,", "∀ Y ≥ Y₀, ∃ C : ℝ, 0 < C ∧", 1
        )
        fixture = ("\n" * (anchor["lines"][0] - 1) + weakened + "\n").encode("utf-8")
        repinned = dict(self.registry["sources"][0], bytes=len(fixture), sha256=hashlib.sha256(fixture).hexdigest(),
                        anchors=[anchor])
        with self.assertRaisesRegex(ValueError, "source anchor mismatch.*stage1"):
            checker.check_source(repinned, fixture)


if __name__ == "__main__":
    unittest.main()
