"""Tests for invalid file data handling (execution must continue)."""

from __future__ import annotations

import io
import sys
import tempfile
import unittest
from pathlib import Path

from reservation_system.storage import JsonStorage
from reservation_system.models import Hotel


class TestInvalidFileData(unittest.TestCase):
    """Ensure invalid JSON or schema does not crash."""

    def test_invalid_json_returns_empty_and_prints_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hotels.json"
            path.write_text("{not-json", encoding="utf-8")
            storage = JsonStorage(path)

            stderr = io.StringIO()
            old_stderr = sys.stderr
            sys.stderr = stderr
            try:
                records = storage.load_records()
            finally:
                sys.stderr = old_stderr

            self.assertEqual(records, [])
            self.assertIn("Invalid JSON", stderr.getvalue())

    def test_invalid_schema_returns_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hotels.json"
            path.write_text('{"not": "a list"}', encoding="utf-8")
            storage = JsonStorage(path)

            stderr = io.StringIO()
            old_stderr = sys.stderr
            sys.stderr = stderr
            try:
                records = storage.load_records()
            finally:
                sys.stderr = old_stderr

            self.assertEqual(records, [])
            self.assertIn("expected JSON array", stderr.getvalue())

    def test_invalid_items_are_skipped_and_execution_continues(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hotels.json"
            # One valid item, one invalid (not a dict), one invalid dict (bad rooms)
            path.write_text(
                '[{"hotel_id":"1","name":"A","city":"X","total_rooms":2,'
                '"available_rooms":2},'
                '"oops",'
                '{"hotel_id":"2","name":"B","city":"Y","total_rooms":1,'
                '"available_rooms":5}]',
                encoding="utf-8",
            )
            storage = JsonStorage(path)

            stderr = io.StringIO()
            old_stderr = sys.stderr
            sys.stderr = stderr
            try:
                hotels = storage.load_objects(Hotel.from_dict)
            finally:
                sys.stderr = old_stderr

            self.assertEqual(len(hotels), 1)
            self.assertEqual(hotels[0].hotel_id, "1")
            out = stderr.getvalue()
            self.assertIn("Skipping invalid item", out)
            self.assertIn("Invalid record", out)
