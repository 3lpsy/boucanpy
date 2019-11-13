#! /usr/bin/env bash
set -e

pytest tests

# pytest -s tests
# pytest --cov=boucanpy --cov-config=.coveragerc tests