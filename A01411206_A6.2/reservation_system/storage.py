"""Persistence helpers for storing objects in JSON files.

The assignment requires:
- Persistent behaviors stored in files
- Ability to handle invalid data in the file without crashing
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable, List, TypeVar

T = TypeVar("T")


class JsonStorage:
    """A tiny JSON storage for lists of records.

    The file format is a JSON array of objects, e.g.:
    [
      {"id": "...", ...},
      {"id": "...", ...}
    ]
    """

    def __init__(self, path: Path) -> None:
        self._path = path

    @property
    def path(self) -> Path:
        """Return the underlying file path."""
        return self._path

    def load_records(self) -> List[dict[str, Any]]:
        """Load a list of dictionaries from file.

        - If file doesn't exist: returns empty list.
        - If file contains invalid JSON or invalid schema: prints error and
          returns empty list.
        Execution continues (required by the assignment).
        """
        if not self._path.exists():
            return []

        try:
            raw_text = self._path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"[storage] Could not read '{self._path}': {exc}", file=sys.stderr)
            return []

        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            print(f"[storage] Invalid JSON in '{self._path}': {exc}", file=sys.stderr)
            return []

        if not isinstance(data, list):
            print(
                f"[storage] Invalid schema in '{self._path}': expected JSON array.",
                file=sys.stderr,
            )
            return []

        valid: List[dict[str, Any]] = []
        for idx, item in enumerate(data):
            if isinstance(item, dict):
                valid.append(item)
            else:
                print(
                    (
                        f"[storage] Skipping invalid item at index {idx} "
                        f"in '{self._path}'."
                    ),
                    file=sys.stderr,
                )

        return valid

    def save_records(self, records: List[dict[str, Any]]) -> None:
        """Save records to file as formatted JSON."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        serialized = json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True)
        self._path.write_text(serialized + "\n", encoding="utf-8")

    def load_objects(self, factory: Callable[[dict[str, Any]], T]) -> List[T]:
        """Load objects using a validating factory.

        Invalid items are skipped with an error message, but execution continues.
        """
        objects: List[T] = []
        for idx, record in enumerate(self.load_records()):
            try:
                objects.append(factory(record))
            except ValueError as exc:
                print(
                    f"[storage] Invalid record at index {idx} in '{self._path}': {exc}",
                    file=sys.stderr,
                )
        return objects

    def save_objects(self, objects: List[Any]) -> None:
        """Save objects that implement to_dict()."""
        records: List[dict[str, Any]] = []
        for obj in objects:
            record = getattr(obj, "to_dict", None)
            if callable(record):
                records.append(record())
            else:
                raise ValueError("Object does not implement to_dict().")
        self.save_records(records)
