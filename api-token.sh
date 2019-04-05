#!/bin/bash

set -e;

docker run --rm \
    --name bountydns-api-token \
    --env-file .env/api.env \
    3lpsy/bountydns:latest \
    api-token-create $@
