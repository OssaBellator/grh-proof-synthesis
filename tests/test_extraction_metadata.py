"""Offline checks for the extraction's pins and source reader."""
import hashlib
import io
import json
import tomllib
import unittest
from unittest.mock import patch

from tools import check_entrypoint_sources as sources


class ExtractionMetadataTests(unittest.TestCase):
    def test_lake_pins(self):
        project = sources.EXTRACTION.parent
        self.assertEqual(
            (project / "lean-toolchain").read_text(encoding="utf-8").strip(),
            "leanprover/lean4:v4.33.1",
        )
        config = tomllib.loads((project / "lakefile.toml").read_text(encoding="utf-8"))
        manifest = json.loads((project / "lake-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(config["require"]), 1)
        requirement = config["require"][0]
        self.assertEqual(requirement["name"], "mathlib")
        self.assertEqual(requirement["rev"], sources.MATHLIB_REVISION)
        package = next(p for p in manifest["packages"] if p["name"] == "mathlib")
        self.assertEqual(package["rev"], requirement["rev"])
        self.assertEqual(package["url"], requirement["git"])

    def test_reader_checks_raw_hash_before_normalizing_line_endings(self):
        data = b"a\r\nb\r\n"
        digest = hashlib.sha256(data).hexdigest()
        with patch.object(sources, "urlopen", return_value=io.BytesIO(data)):
            self.assertEqual(sources.read_pinned_source("https://example.com", len(data), digest), "a\nb")
        for modified in (b"c\r\nb\r\n", data + b"x"):
            with self.subTest(data=modified):
                with patch.object(sources, "urlopen", return_value=io.BytesIO(modified)):
                    with self.assertRaisesRegex(SystemExit, "Source identity mismatch"):
                        sources.read_pinned_source("https://example.com", len(data), digest)
