"""Regression tests for research metadata, not GRH."""
import copy
import json
import unittest
from pathlib import Path

from tools.validate_claims import LEDGER, validate_records


class ClaimLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(Path(LEDGER).read_text(encoding="utf-8"))

    def test_repository_ledger_passes(self):
        self.assertEqual(validate_records(self.ledger), [])

    def test_duplicate_claim_id_is_rejected(self):
        broken = copy.deepcopy(self.ledger)
        broken["claims"].append(copy.deepcopy(broken["claims"][0]))
        self.assertTrue(any("duplicate id" in item for item in validate_records(broken)))

    def test_missing_source_is_rejected(self):
        broken = copy.deepcopy(self.ledger)
        broken["claims"][0]["source_urls"] = []
        self.assertTrue(any("source_urls" in item for item in validate_records(broken)))

    def test_invalid_status_is_rejected(self):
        broken = copy.deepcopy(self.ledger)
        broken["claims"][0]["status"] = "proved-by-AI"
        self.assertTrue(any("unknown status" in item for item in validate_records(broken)))


if __name__ == "__main__":
    unittest.main()
