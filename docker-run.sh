#!/bin/sh

set -e

BDBSCTL="/bountydns/bdnsctl.py"
echo "[+] running: python3 $BDBSCTL $@"
exec python3 $BDBSCTL $@
