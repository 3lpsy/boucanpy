#!/bin/sh

set -e

BDBSCTL="/boucanpy/bdnsctl.py"
echo "[+] running: python3 $BDBSCTL $@"
exec python3 $BDBSCTL $@
