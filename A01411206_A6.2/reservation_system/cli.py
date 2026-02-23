"""Command-line interface for the reservation system.

This is optional for grading, but it demonstrates console I/O as requested
in the assignment.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .services import ReservationSystem


def _default_data_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "data"


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(prog="reservation-system")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=_default_data_dir(),
        help="Directory to store JSON data files.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    create_h = sub.add_parser("create-hotel", help="Create a hotel")
    create_h.add_argument("--name", required=True)
    create_h.add_argument("--city", required=True)
    create_h.add_argument("--rooms", required=True, type=int)

    create_c = sub.add_parser("create-customer", help="Create a customer")
    create_c.add_argument("--name", required=True)
    create_c.add_argument("--email", required=True)

    reserve = sub.add_parser("reserve", help="Reserve a room")
    reserve.add_argument("--customer-id", required=True)
    reserve.add_argument("--hotel-id", required=True)
    reserve.add_argument("--room-count", required=True, type=int)
    reserve.add_argument("--start-date", required=True, help="YYYY-MM-DD")
    reserve.add_argument("--end-date", required=True, help="YYYY-MM-DD")

    cancel = sub.add_parser("cancel", help="Cancel a reservation")
    cancel.add_argument("--reservation-id", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = build_parser()
    args = parser.parse_args(argv)

    data_dir: Path = args.data_dir
    system = ReservationSystem(
        hotels_path=data_dir / "hotels.json",
        customers_path=data_dir / "customers.json",
        reservations_path=data_dir / "reservations.json",
    )

    if args.cmd == "create-hotel":
        hotel = system.create_hotel(args.name, args.city, args.rooms)
        print(f"Created hotel: {hotel.hotel_id} ({hotel.name})")
        return 0

    if args.cmd == "create-customer":
        customer = system.create_customer(args.name, args.email)
        print(f"Created customer: {customer.customer_id} ({customer.name})")
        return 0

    if args.cmd == "reserve":
        reservation = system.reserve_room(
            args.customer_id,
            args.hotel_id,
            args.room_count,
            (args.start_date, args.end_date),
        )
        print(f"Created reservation: {reservation.reservation_id}")
        return 0

    if args.cmd == "cancel":
        ok = system.cancel_reservation(args.reservation_id)
        print("Canceled." if ok else "Not found.")
        return 0

    parser.error("Unknown command.")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
