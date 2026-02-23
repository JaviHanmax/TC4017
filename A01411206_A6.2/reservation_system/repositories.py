"""Repositories: CRUD operations using file persistence."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import List, Optional

from .models import Customer, Hotel, Reservation
from .storage import JsonStorage


class HotelRepository:
    """CRUD repository for hotels."""

    def __init__(self, path: Path) -> None:
        self._storage = JsonStorage(path)

    def list_all(self) -> List[Hotel]:
        """Return all hotels."""
        return self._storage.load_objects(Hotel.from_dict)

    def get(self, hotel_id: str) -> Optional[Hotel]:
        """Get a hotel by id, or None."""
        return next((h for h in self.list_all() if h.hotel_id == hotel_id), None)

    def upsert(self, hotel: Hotel) -> None:
        """Insert or update a hotel."""
        hotels = self.list_all()
        updated = [h for h in hotels if h.hotel_id != hotel.hotel_id]
        updated.append(hotel)
        self._storage.save_objects(updated)

    def delete(self, hotel_id: str) -> bool:
        """Delete a hotel. Returns True if it existed."""
        hotels = self.list_all()
        remaining = [h for h in hotels if h.hotel_id != hotel_id]
        existed = len(remaining) != len(hotels)
        self._storage.save_objects(remaining)
        return existed

    def modify(
        self,
        hotel_id: str,
        *,
        name: str | None = None,
        city: str | None = None,
        total_rooms: int | None = None,
    ) -> Hotel:
        """Modify a hotel's info and return the updated hotel."""
        hotel = self.get(hotel_id)
        if hotel is None:
            raise ValueError("Hotel not found.")

        new_total = hotel.total_rooms if total_rooms is None else total_rooms
        if new_total < 0:
            raise ValueError("total_rooms must be >= 0.")

        # Keep availability consistent:
        delta_total = new_total - hotel.total_rooms
        new_available = hotel.available_rooms + delta_total
        if new_available < 0:
            raise ValueError("Cannot reduce total_rooms below reserved rooms.")

        updated = replace(
            hotel,
            name=hotel.name if name is None else name,
            city=hotel.city if city is None else city,
            total_rooms=new_total,
            available_rooms=new_available,
        )
        self.upsert(updated)
        return updated


class CustomerRepository:
    """CRUD repository for customers."""

    def __init__(self, path: Path) -> None:
        self._storage = JsonStorage(path)

    def list_all(self) -> List[Customer]:
        """Return all customers."""
        return self._storage.load_objects(Customer.from_dict)

    def get(self, customer_id: str) -> Optional[Customer]:
        """Get a customer by id, or None."""
        return next(
            (c for c in self.list_all() if c.customer_id == customer_id), None
        )

    def upsert(self, customer: Customer) -> None:
        """Insert or update a customer."""
        customers = self.list_all()
        updated = [c for c in customers if c.customer_id != customer.customer_id]
        updated.append(customer)
        self._storage.save_objects(updated)

    def delete(self, customer_id: str) -> bool:
        """Delete a customer. Returns True if it existed."""
        customers = self.list_all()
        remaining = [c for c in customers if c.customer_id != customer_id]
        existed = len(remaining) != len(customers)
        self._storage.save_objects(remaining)
        return existed

    def modify(
        self,
        customer_id: str,
        *,
        name: str | None = None,
        email: str | None = None,
    ) -> Customer:
        """Modify a customer's info and return the updated customer."""
        customer = self.get(customer_id)
        if customer is None:
            raise ValueError("Customer not found.")
        updated = replace(
            customer,
            name=customer.name if name is None else name,
            email=customer.email if email is None else email,
        )
        self.upsert(updated)
        return updated


class ReservationRepository:
    """CRUD repository for reservations."""

    def __init__(self, path: Path) -> None:
        self._storage = JsonStorage(path)

    def list_all(self) -> List[Reservation]:
        """Return all reservations."""
        return self._storage.load_objects(Reservation.from_dict)

    def get(self, reservation_id: str) -> Optional[Reservation]:
        """Get a reservation by id, or None."""
        return next(
            (r for r in self.list_all() if r.reservation_id == reservation_id),
            None,
        )

    def upsert(self, reservation: Reservation) -> None:
        """Insert or update a reservation."""
        reservations = self.list_all()
        updated = [
            r for r in reservations if r.reservation_id != reservation.reservation_id
        ]
        updated.append(reservation)
        self._storage.save_objects(updated)

    def delete(self, reservation_id: str) -> bool:
        """Delete a reservation. Returns True if it existed."""
        reservations = self.list_all()
        remaining = [r for r in reservations if r.reservation_id != reservation_id]
        existed = len(remaining) != len(reservations)
        self._storage.save_objects(remaining)
        return existed

    def for_hotel(self, hotel_id: str) -> List[Reservation]:
        """List reservations for a given hotel."""
        return [r for r in self.list_all() if r.hotel_id == hotel_id]

    def for_customer(self, customer_id: str) -> List[Reservation]:
        """List reservations for a given customer."""
        return [r for r in self.list_all() if r.customer_id == customer_id]
