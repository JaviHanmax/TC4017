"""High-level orchestration for the reservation system."""

from __future__ import annotations

import uuid
from dataclasses import replace
from datetime import date
from pathlib import Path

from .models import Customer, Hotel, Reservation
from .repositories import CustomerRepository, HotelRepository, ReservationRepository


class ReservationSystem:
    """Facade service implementing the required behaviors."""

    def __init__(
        self,
        hotels_path: Path,
        customers_path: Path,
        reservations_path: Path,
    ) -> None:
        self.hotels = HotelRepository(hotels_path)
        self.customers = CustomerRepository(customers_path)
        self.reservations = ReservationRepository(reservations_path)

    # ------------------------
    # Hotel behaviors
    # ------------------------
    def create_hotel(self, name: str, city: str, total_rooms: int) -> Hotel:
        """Create and persist a new hotel."""
        if total_rooms < 0:
            raise ValueError("total_rooms must be >= 0.")
        hotel = Hotel(
            hotel_id=str(uuid.uuid4()),
            name=name.strip(),
            city=city.strip(),
            total_rooms=total_rooms,
            available_rooms=total_rooms,
        )
        self.hotels.upsert(hotel)
        return hotel

    def delete_hotel(self, hotel_id: str) -> bool:
        """Delete a hotel if it has no active reservations."""
        if self.reservations.for_hotel(hotel_id):
            raise ValueError("Cannot delete hotel with active reservations.")
        return self.hotels.delete(hotel_id)

    def display_hotel(self, hotel_id: str) -> Hotel:
        """Return hotel info."""
        hotel = self.hotels.get(hotel_id)
        if hotel is None:
            raise ValueError("Hotel not found.")
        return hotel

    def modify_hotel(
        self,
        hotel_id: str,
        *,
        name: str | None = None,
        city: str | None = None,
        total_rooms: int | None = None,
    ) -> Hotel:
        """Modify and persist hotel info."""
        return self.hotels.modify(
            hotel_id,
            name=name,
            city=city,
            total_rooms=total_rooms,
        )

    def reserve_room(
        self,
        customer_id: str,
        hotel_id: str,
        room_count: int,
        date_range: tuple[str, str],
    ) -> Reservation:
        """Reserve one or more rooms for a customer in a hotel."""
        if room_count < 1:
            raise ValueError("room_count must be >= 1.")

        if self.customers.get(customer_id) is None:
            raise ValueError("Customer not found.")
        hotel = self.hotels.get(hotel_id)
        if hotel is None:
            raise ValueError("Hotel not found.")

        start_date, end_date = date_range
        # Validate dates:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
        if end < start:
            raise ValueError("end_date must be >= start_date.")

        if hotel.available_rooms < room_count:
            raise ValueError("Not enough available rooms.")

        # Update hotel inventory:
        updated_hotel = replace(
            hotel, available_rooms=hotel.available_rooms - room_count)
        self.hotels.upsert(updated_hotel)

        # Create reservation:
        reservation = Reservation(
            reservation_id=str(uuid.uuid4()),
            customer_id=customer_id,
            hotel_id=hotel_id,
            room_count=room_count,
            start_date=start_date,
            end_date=end_date,
        )
        self.reservations.upsert(reservation)
        return reservation

    def cancel_reservation(self, reservation_id: str) -> bool:
        """Cancel a reservation and restore hotel inventory."""
        reservation = self.reservations.get(reservation_id)
        if reservation is None:
            return False

        hotel = self.hotels.get(reservation.hotel_id)
        if hotel is None:
            # Edge case: hotel was deleted externally; still delete reservation.
            self.reservations.delete(reservation_id)
            return True

        updated_hotel = replace(
            hotel, available_rooms=hotel.available_rooms + reservation.room_count
        )
        self.hotels.upsert(updated_hotel)
        self.reservations.delete(reservation_id)
        return True

    # ------------------------
    # Customer behaviors
    # ------------------------
    def create_customer(self, name: str, email: str) -> Customer:
        """Create and persist a new customer."""
        customer = Customer(
            customer_id=str(uuid.uuid4()),
            name=name.strip(),
            email=email.strip(),
        )
        self.customers.upsert(customer)
        return customer

    def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer if they have no active reservations."""
        if self.reservations.for_customer(customer_id):
            raise ValueError("Cannot delete customer with active reservations.")
        return self.customers.delete(customer_id)

    def display_customer(self, customer_id: str) -> Customer:
        """Return customer info."""
        customer = self.customers.get(customer_id)
        if customer is None:
            raise ValueError("Customer not found.")
        return customer

    def modify_customer(
        self,
        customer_id: str,
        *,
        name: str | None = None,
        email: str | None = None,
    ) -> Customer:
        """Modify and persist customer info."""
        return self.customers.modify(customer_id, name=name, email=email)
