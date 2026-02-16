#!/usr/bin/env python3
"""
computeSales.py

Computes the total cost for all sales contained in a sales record JSON file,
using a price catalogue JSON file.

Usage:
    python computeSales.py priceCatalogue.json salesRecord.json

Results are printed to the console and written to SalesResults.txt.
Errors are reported to the console and execution continues when possible.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple


@dataclass(frozen=True)
class LineItem:
    """A single sales line item."""

    product: str
    quantity: Decimal
    path: str  # Human-readable location of the item in the JSON structure


def _eprint(message: str) -> None:
    """Print a message to stderr."""
    print(message, file=sys.stderr)


def _to_decimal(value: Any, *, context: str) -> Optional[Decimal]:
    """Convert a value to Decimal, returning None if it cannot be converted."""
    try:
        if isinstance(value, Decimal):
            return value
        if isinstance(value, (int, float, str)):
            return Decimal(str(value))
    except (InvalidOperation, ValueError):
        _eprint(f"[ERROR] Invalid numeric value at {context}: {value!r}")
        return None

    _eprint(f"[ERROR] Expected numeric value at {context}, got: {type(value).__name__}")
    return None


def load_json(path: Path) -> Any:
    """Load JSON from a file. On error, report and return an empty structure."""
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        _eprint(f"[ERROR] File not found: {path}")
    except json.JSONDecodeError as exc:
        _eprint(f"[ERROR] Invalid JSON in file {path}: {exc}")
    except OSError as exc:
        _eprint(f"[ERROR] Could not read file {path}: {exc}")

    # Continue execution with an empty structure.
    return {}


def parse_price_catalogue(data: Any) -> Dict[str, Decimal]:
    """
    Parse a catalogue of prices.

    Supported formats:
    - {"productA": 10.5, "productB": 7}
    - [{"product": "productA", "price": 10.5}, {"name": "productB", "cost": 7}]
    """
    prices: Dict[str, Decimal] = {}

    if isinstance(data, dict):
        # Mapping of product -> price
        for key, value in data.items():
            if not isinstance(key, str):
                _eprint(f"[ERROR] Catalogue key is not a string: {key!r}")
                continue
            price = _to_decimal(value, context=f"catalogue[{key!r}]")
            if price is None:
                continue
            prices[key] = price
        return prices

    if isinstance(data, list):
        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                _eprint(f"[ERROR] Catalogue entry at index {idx} is not an object: {item!r}")
                continue

            lower_keys = {str(k).lower(): k for k in item.keys()}
            product_key = (
                lower_keys.get("product")
                or lower_keys.get("name")
                or lower_keys.get("title")
                or lower_keys.get("id")
                or lower_keys.get("sku")
            )
            price_key = lower_keys.get("price") or lower_keys.get("cost") or lower_keys.get("value")

            if product_key is None or price_key is None:
                _eprint(f"[ERROR] Catalogue entry missing product/price at index {idx}: {item!r}")
                continue

            product_value = item[product_key]
            if not isinstance(product_value, str):
                _eprint(f"[ERROR] Catalogue product is not a string at index {idx}: {product_value!r}")
                continue

            price = _to_decimal(item[price_key], context=f"catalogue[{idx}].{price_key}")
            if price is None:
                continue

            prices[product_value] = price

        return prices

    _eprint(f"[ERROR] Unsupported price catalogue format: {type(data).__name__}")
    return prices


def _looks_like_product_quantity_map(data: dict) -> bool:
    """
    Heuristic: a dict that maps product-name -> quantity.

    Important: avoid misclassifying line-item objects such as
    {"product": "...", "quantity": ...}.
    """
    if not data:
        return False

    lower_keys = {str(k).lower() for k in data.keys()}

    # If it contains typical container keys, it's not a flat map.
    if lower_keys.intersection({"items", "products", "sales", "records"}):
        return False

    # If it contains typical line-item keys, it's not a flat map.
    if lower_keys.intersection(
        {
            "product",
            "name",
            "title",
            "sku",
            "id",
            "quantity",
            "qty",
            "count",
            "units",
            "price",
            "cost",
            "value",
        }
    ):
        return False

    return all(isinstance(k, str) for k in data.keys()) and all(
        isinstance(v, (int, float, str, Decimal)) for v in data.values()
    )


def _extract_line_item(obj: dict, path: str) -> Optional[LineItem]:
    """Try to extract a LineItem from a dict object."""
    key_map = {str(k).lower(): k for k in obj.keys()}
    product_key = (
        key_map.get("product")
        or key_map.get("name")
        or key_map.get("title")
        or key_map.get("sku")
        or key_map.get("id")
    )
    quantity_key = key_map.get("quantity") or key_map.get("qty") or key_map.get("count") or key_map.get("units")

    if product_key is None or quantity_key is None:
        return None

    product_value = obj[product_key]
    if not isinstance(product_value, str):
        _eprint(f"[ERROR] Invalid product value at {path}.{product_key}: {product_value!r}")
        return None

    quantity = _to_decimal(obj[quantity_key], context=f"{path}.{quantity_key}")
    if quantity is None:
        return None

    if quantity <= 0:
        _eprint(f"[ERROR] Quantity must be > 0 at {path}.{quantity_key}: {quantity}")
        return None

    return LineItem(product=product_value, quantity=quantity, path=path)


def iter_line_items(data: Any, *, path: str = "$") -> Iterator[LineItem]:
    """
    Iterate over all line items inside an arbitrary JSON structure.

    This function is intentionally tolerant: it searches for objects that look like
    {"product": "...", "quantity": ...} in nested lists/dicts, and also supports
    a flat mapping like {"productA": 2, "productB": 1}.
    """
    if isinstance(data, list):
        for idx, value in enumerate(data):
            yield from iter_line_items(value, path=f"{path}[{idx}]")
        return

    if isinstance(data, dict):
        if _looks_like_product_quantity_map(data):
            for product, qty in data.items():
                quantity = _to_decimal(qty, context=f"{path}[{product!r}]")
                if quantity is None:
                    continue
                if quantity <= 0:
                    _eprint(f"[ERROR] Quantity must be > 0 at {path}[{product!r}]: {quantity}")
                    continue
                yield LineItem(product=product, quantity=quantity, path=f"{path}[{product!r}]")
            return

        maybe_item = _extract_line_item(data, path)
        if maybe_item is not None:
            yield maybe_item
            # Do not return: sometimes line item objects contain extra nested structures.
            # We'll keep scanning for any nested items.
        for key, value in data.items():
            key_str = str(key)
            yield from iter_line_items(value, path=f"{path}.{key_str}")
        return

    # Scalars are ignored.


def compute_total(prices: Dict[str, Decimal], sales_data: Any) -> Tuple[Decimal, int, int]:
    """
    Compute total cost for all sales.

    Returns:
        (total_cost, processed_items, skipped_items)
    """
    total = Decimal("0")
    processed = 0
    skipped = 0

    for item in iter_line_items(sales_data):
        processed += 1
        if item.product not in prices:
            skipped += 1
            _eprint(f"[ERROR] Unknown product at {item.path}: {item.product!r}")
            continue

        total += prices[item.product] * item.quantity

    return total, processed, skipped


def format_money(value: Decimal) -> str:
    """Format a Decimal amount using 2 decimal places."""
    quantized = value.quantize(Decimal("0.01"))
    return f"{quantized:,.2f}"


def build_report(
    *,
    price_file: Path,
    sales_file: Path,
    total_cost: Decimal,
    processed_items: int,
    skipped_items: int,
    elapsed_seconds: float,
) -> str:
    """Create a human-readable report."""
    lines: List[str] = [
        "Sales Results",
        "=============",
        "",
        f"Price catalogue file: {price_file}",
        f"Sales record file:   {sales_file}",
        "",
        f"Line items processed: {processed_items}",
        f"Line items skipped:   {skipped_items}",
        "",
        f"TOTAL COST: {format_money(total_cost)}",
        "",
        f"Time elapsed: {elapsed_seconds:.6f} seconds",
        "",
        "Notes:",
        "- Any invalid entries are reported to the console and skipped.",
        "- Total cost is computed as sum(price(product) * quantity) for each valid line item.",
    ]
    return "\n".join(lines)


def write_results(report: str, output_path: Path) -> None:
    """Write report to output file."""
    try:
        output_path.write_text(report, encoding="utf-8")
    except OSError as exc:
        _eprint(f"[ERROR] Could not write results file {output_path}: {exc}")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Compute total cost of sales from JSON files.")
    parser.add_argument("price_catalogue", help="Path to priceCatalogue.json")
    parser.add_argument("sales_record", help="Path to salesRecord.json")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    """Program entry point."""
    args = parse_args(argv)
    price_path = Path(args.price_catalogue)
    sales_path = Path(args.sales_record)

    start = time.perf_counter()

    price_data = load_json(price_path)
    sales_data = load_json(sales_path)

    prices = parse_price_catalogue(price_data)
    if not prices:
        _eprint("[ERROR] Price catalogue is empty or invalid. Totals may be zero.")

    total, processed, skipped = compute_total(prices, sales_data)

    elapsed = time.perf_counter() - start

    report = build_report(
        price_file=price_path,
        sales_file=sales_path,
        total_cost=total,
        processed_items=processed,
        skipped_items=skipped,
        elapsed_seconds=elapsed,
    )

    print(report)
    write_results(report, Path("SalesResults.txt"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
