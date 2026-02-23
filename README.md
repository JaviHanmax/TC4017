# Activity 6.2 — Reservation System (Exercise 3)

This repository implements a simple **Reservation System** with three abstractions:

- **Hotel**
- **Customer**
- **Reservation**

It includes file persistence (JSON files), error handling for invalid file data, and unit tests with **≥85% line coverage**, per the assignment requirements. fileciteturn0file0

## Project structure

```
reservation_system/
  models.py         # Hotel, Customer, Reservation (dataclasses)
  storage.py        # JSON persistence + invalid data handling
  repositories.py   # CRUD repositories
  services.py       # ReservationSystem facade
  cli.py            # Optional CLI (console I/O)
tests/
  test_system.py
  test_storage_invalid.py
data/
  hotels.json
  customers.json
  reservations.json
```

> Replace the folder name `A01411206_A6.2` with **your own** `Matrícula_A6.2` as requested.

## Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
```

## Run unit tests

```bash
python -m unittest -v
```

## Coverage (must be ≥85%)

```bash
coverage run -m unittest
coverage report -m
```

## Static analysis (flake8 + pylint)

```bash
flake8 reservation_system tests
pylint reservation_system
```

## CLI quick demo (optional)

```bash
python -m reservation_system.cli create-hotel --name "Hotel One" --city "Monterrey" --rooms 10
python -m reservation_system.cli create-customer --name "Alice" --email "alice@example.com"
# then reserve/cancel using the printed IDs
```
