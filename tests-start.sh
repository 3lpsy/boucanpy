#! /usr/bin/env bash
set -e

pytest tests

# pytest -s tests
# pytest --cov=bountydns --cov-config=.coveragerc tests