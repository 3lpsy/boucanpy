#!/bin/bash

# TODO: make path to env dynamic
ENV_DIR="$(pwd)/.env"

docker run \
    --rm \
    --env-file $ENV_DIR/core.env \
    --env-file $ENV_DIR/api.env \
    --env-file $ENV_DIR/db.env \
    3lpsy/bountydns $@
