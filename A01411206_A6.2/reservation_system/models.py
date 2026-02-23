"""Domain models used by the reservation system."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Dict


def _require_str(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Invalid '{field_name}': expected non-empty string.")
    return value.strip()


def _require_int(value: Any, field_name: str, *, min_value: int | None = None) -> int:
    if not isinstance(value, int):
        raise ValueError(f"Invalid '{field_name}': expected int.")
    if min_value is not None and value < min_value:
        raise ValueError(f"Invalid '{field_name}': expected >= {min_value}.")
    return value


def _require_iso_date(value: Any, field_name: str) -> str:
    value_str = _require_str(value, field_name)
    # Validate format by attempting to parse.
    try:
        date.fromisoformat(value_str)
    except ValueError as exc:
        msg = (
            f"Invalid '{field_name}': expected ISO date YYYY-MM-DD."
        )
        raise ValueError(msg) from exc
    return value_str


@dataclass(frozen=True, slots=True)
class Hotel:
    """A hotel with a finite inventory of rooms."""

    hotel_id: str
    name: str
    city: str
    total_rooms: int
    available_rooms: int

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a JSON-compatible dictionary."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "city": self.city,
            "total_rooms": self.total_rooms,
            "available_rooms": self.available_rooms,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Hotel":
        """Deserialize from a dictionary, validating required fields."""
        if not isinstance(data, dict):
            raise ValueError("Invalid hotel record: expected object.")
        hotel_id = _require_str(data.get("hotel_id"), "hotel_id")
        name = _require_str(data.get("name"), "name")
        city = _require_str(data.get("city"), "city")
        total_rooms = _require_int(data.get("total_rooms"), "total_rooms", min_value=0)
        available_rooms = _require_int(
            data.get("available_rooms"), "available_rooms", min_value=0
        )
        if available_rooms > total_rooms:
            raise ValueError("Invalid 'available_rooms': cannot exceed total_rooms.")
        return cls(
            hotel_id=hotel_id,
            name=name,
            city=city,
            total_rooms=total_rooms,
            available_rooms=available_rooms,
        )


@dataclass(frozen=True, slots=True)
class Customer:
    """A customer who can make reservations."""

    customer_id: str
    name: str
    email: str

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a JSON-compatible dictionary."""
        return {"customer_id": self.customer_id, "name": self.name, "email": self.email}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Customer":
        """Deserialize from a dictionary, validating required fields."""
        if not isinstance(data, dict):
            raise ValueError("Invalid customer record: expected object.")
        customer_id = _require_str(data.get("customer_id"), "customer_id")
        name = _require_str(data.get("name"), "name")
        email = _require_str(data.get("email"), "email")
        return cls(customer_id=customer_id, name=name, email=email)


@dataclass(frozen=True, slots=True)
class Reservation:
    """A reservation linking a customer and a hotel."""

    reservation_id: str
    customer_id: str
    hotel_id: str
    room_count: int
    start_date: str
    end_date: str

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a JSON-compatible dictionary."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
            "room_count": self.room_count,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Reservation":
        """Deserialize from a dictionary, validating required fields."""
        if not isinstance(data, dict):
            raise ValueError("Invalid reservation record: expected object.")
        reservation_id = _require_str(data.get("reservation_id"), "reservation_id")
        customer_id = _require_str(data.get("customer_id"), "customer_id")
        hotel_id = _require_str(data.get("hotel_id"), "hotel_id")
        room_count = _require_int(data.get("room_count"), "room_count", min_value=1)
        start_date = _require_iso_date(data.get("start_date"), "start_date")
        end_date = _require_iso_date(data.get("end_date"), "end_date")
        if date.fromisoformat(end_date) < date.fromisoformat(start_date):
            raise ValueError("Invalid date range: end_date must be >= start_date.")
        return cls(
            reservation_id=reservation_id,
            customer_id=customer_id,
            hotel_id=hotel_id,
            room_count=room_count,
            start_date=start_date,
            end_date=end_date,
        )
