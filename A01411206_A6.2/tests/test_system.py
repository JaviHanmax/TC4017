"""End-to-end unit tests for ReservationSystem."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from reservation_system.services import ReservationSystem


class TestReservationSystem(unittest.TestCase):
    """Test the required behaviors for hotels, customers, reservations."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        data_dir = Path(self._tmp.name)
        self.system = ReservationSystem(
            hotels_path=data_dir / "hotels.json",
            customers_path=data_dir / "customers.json",
            reservations_path=data_dir / "reservations.json",
        )

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_create_display_modify_delete_customer(self) -> None:
        customer = self.system.create_customer("Alice", "alice@example.com")
        loaded = self.system.display_customer(customer.customer_id)
        self.assertEqual(loaded.email, "alice@example.com")

        updated = self.system.modify_customer(customer.customer_id, name="Alicia")
        self.assertEqual(updated.name, "Alicia")

        deleted = self.system.delete_customer(customer.customer_id)
        self.assertTrue(deleted)

    def test_create_display_modify_delete_hotel(self) -> None:
        hotel = self.system.create_hotel("Hotel One", "Monterrey", 10)
        loaded = self.system.display_hotel(hotel.hotel_id)
        self.assertEqual(loaded.available_rooms, 10)

        updated = self.system.modify_hotel(hotel.hotel_id, total_rooms=12)
        self.assertEqual(updated.total_rooms, 12)
        self.assertEqual(updated.available_rooms, 12)

        deleted = self.system.delete_hotel(hotel.hotel_id)
        self.assertTrue(deleted)

    def test_reserve_and_cancel_reservation_updates_inventory(self) -> None:
        hotel = self.system.create_hotel("Hotel One", "Monterrey", 3)
        customer = self.system.create_customer("Bob", "bob@example.com")

        reservation = self.system.reserve_room(
            customer.customer_id,
            hotel.hotel_id,
            2,
            ("2026-01-01", "2026-01-03"),
        )
        hotel_after = self.system.display_hotel(hotel.hotel_id)
        self.assertEqual(hotel_after.available_rooms, 1)

        ok = self.system.cancel_reservation(reservation.reservation_id)
        self.assertTrue(ok)
        hotel_final = self.system.display_hotel(hotel.hotel_id)
        self.assertEqual(hotel_final.available_rooms, 3)

    def test_reserve_fails_when_not_enough_rooms(self) -> None:
        hotel = self.system.create_hotel("Hotel One", "Monterrey", 1)
        customer = self.system.create_customer("Bob", "bob@example.com")
        self.system.reserve_room(
            customer.customer_id,
            hotel.hotel_id,
            1,
            ("2026-01-01", "2026-01-02"),
        )
        with self.assertRaises(ValueError):
            self.system.reserve_room(
                customer.customer_id,
                hotel.hotel_id,
                1,
                ("2026-01-01", "2026-01-02"),
            )

    def test_delete_hotel_or_customer_with_active_reservation_fails(self) -> None:
        hotel = self.system.create_hotel("Hotel One", "Monterrey", 2)
        customer = self.system.create_customer("Bob", "bob@example.com")
        reservation = self.system.reserve_room(
            customer.customer_id,
            hotel.hotel_id,
            1,
            ("2026-01-01", "2026-01-02"),
        )
        self.assertIsNotNone(reservation.reservation_id)

        with self.assertRaises(ValueError):
            self.system.delete_hotel(hotel.hotel_id)

        with self.assertRaises(ValueError):
            self.system.delete_customer(customer.customer_id)

    def test_cancel_unknown_reservation_returns_false(self) -> None:
        ok = self.system.cancel_reservation("missing")
        self.assertFalse(ok)

    def test_modify_hotel_total_rooms_cannot_go_below_reserved(self) -> None:
        hotel = self.system.create_hotel("Hotel One", "Monterrey", 2)
        customer = self.system.create_customer("Bob", "bob@example.com")
        self.system.reserve_room(
            customer.customer_id,
            hotel.hotel_id,
            2,
            ("2026-01-01", "2026-01-02"),
        )
        with self.assertRaises(ValueError):
            self.system.modify_hotel(hotel.hotel_id, total_rooms=1)

    def test_reserve_requires_valid_dates(self) -> None:
        hotel = self.system.create_hotel("Hotel One", "Monterrey", 1)
        customer = self.system.create_customer("Bob", "bob@example.com")
        with self.assertRaises(ValueError):
            self.system.reserve_room(
                customer.customer_id,
                hotel.hotel_id,
                1,
                ("2026-01-03", "2026-01-01"),
            )
