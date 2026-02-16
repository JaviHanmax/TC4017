import json
import unittest
from decimal import Decimal
from pathlib import Path

import computeSales


class TestComputeSales(unittest.TestCase):
    def setUp(self):
        self.prices = {
            "a": Decimal("10.00"),
            "b": Decimal("2.50"),
        }

    def test_iter_line_items_finds_nested_items(self):
        data = [{"sale": {"items": [{"product": "a", "quantity": 2}, {"product": "b", "quantity": 1}]}}]
        items = list(computeSales.iter_line_items(data))
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].product, "a")
        self.assertEqual(items[0].quantity, Decimal("2"))

    def test_iter_line_items_supports_map(self):
        data = {"a": 2, "b": 1}
        items = list(computeSales.iter_line_items(data))
        self.assertEqual({i.product for i in items}, {"a", "b"})

    def test_compute_total_skips_unknown_product(self):
        data = [{"product": "a", "quantity": 2}, {"product": "missing", "quantity": 1}]
        total, processed, skipped = computeSales.compute_total(self.prices, data)
        self.assertEqual(processed, 2)
        self.assertEqual(skipped, 1)
        self.assertEqual(total, Decimal("20.00"))

    def test_parse_price_catalogue_dict(self):
        data = {"a": 10, "b": "2.5"}
        prices = computeSales.parse_price_catalogue(data)
        self.assertEqual(prices["a"], Decimal("10"))
        self.assertEqual(prices["b"], Decimal("2.5"))

    def test_load_json_missing_returns_empty(self):
        missing = computeSales.load_json(Path("does_not_exist.json"))
        self.assertEqual(missing, {})

    def test_end_to_end_example_files(self):
        root = Path(__file__).resolve().parent.parent
        price_path = root / "data" / "priceCatalogue.json"
        sales_path = root / "data" / "salesRecord.json"

        prices = computeSales.parse_price_catalogue(json.loads(price_path.read_text(encoding="utf-8")))
        sales = json.loads(sales_path.read_text(encoding="utf-8"))

        total, processed, skipped = computeSales.compute_total(prices, sales)

        # valid items:
        # sale 1: apple 2*10 + milk 1*27.25 = 47.25
        # sale 2: banana 3*5.5 + bread 1*18 = 34.5
        # total = 81.75
        self.assertEqual(total.quantize(Decimal("0.01")), Decimal("81.75"))
        self.assertEqual(processed, 5)
        self.assertEqual(skipped, 1)


if __name__ == "__main__":
    unittest.main()
