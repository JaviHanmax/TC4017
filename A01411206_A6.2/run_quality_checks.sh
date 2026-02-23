#!/usr/bin/env bash
set -euo pipefail

python -m unittest -v
coverage run -m unittest
coverage report -m

flake8 reservation_system tests
pylint reservation_system
