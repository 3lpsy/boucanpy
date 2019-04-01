#!/bin/sh

set -e

BDBSCTL="/bountydns/bdnsctl.py"

exec python3 $BDBSCTL $@
