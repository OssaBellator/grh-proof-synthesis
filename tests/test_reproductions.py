"""Offline checks on the evidence registry. No upstream checks are replayed."""
import datetime as dt
import json
import unittest
from pathlib import Path
from urllib.parse import urlsplit


REGISTRY = Path(__file__).resolve().parents[1] / "data" / "reproductions.json"
KINDS = {
    "independent_check", "mirror", "commentary", "historical_method",
    "alternate_program", "source_manuscript",
}
TRUST_LEVELS = {"public_run_record", "primary_text"}


class ReproductionRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        cls.records = cls.registry["reproductions"]

    def test_schema_and_identifiers(self):
        self.assertEqual(self.registry["schema_version"], 1)
        self.assertEqual(set(self.registry["trust_levels"]), TRUST_LEVELS)
        self.assertIsInstance(self.records, list)
        self.assertTrue(self.records)
        identifiers = [record["id"] for record in self.records]
        self.assertEqual(len(identifiers), len(set(identifiers)))

    def test_each_record_has_provenance_and_scope(self):
        for record in self.records:
            with self.subTest(record=record["id"]):
                for key in ("id", "author", "source_date", "verified_evidence",
                            "limitations", "potential_use"):
                    self.assertIsInstance(record[key], str)
                    self.assertTrue(record[key].strip(), key)
                day = dt.date.fromisoformat(record["date_checked"])
                self.assertEqual(day.isoformat(), record["date_checked"])
                self.assertIn(record["kind"], KINDS)
                self.assertIn(record["trust_level"], TRUST_LEVELS)
                receipts = record.get("receipts", [])
                self.assertIsInstance(receipts, list)
                for url in [record["source_url"], *receipts]:
                    address = urlsplit(url)
                    self.assertEqual(address.scheme, "https", url)
                    self.assertTrue(address.hostname, url)

    def test_independent_checks_identify_a_public_run_record(self):
        for record in self.records:
            with self.subTest(record=record["id"]):
                if record["kind"] == "independent_check":
                    self.assertEqual(record["trust_level"], "public_run_record")
                elif record["kind"] == "mirror":
                    self.assertEqual(record["trust_level"], "primary_text")
