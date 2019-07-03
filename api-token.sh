#!/bin/bash

set -e;

echo "Building the 3lpsy/bountydns:latest container..."
docker build -f infra/docker/bountydns.dockerfile . -t 3lpsy/bountydns:latest --no-cache

echo "Running the 3lpsy/bountydns:latest container instance to generate a token..."
docker run --rm \
    --name bountydns-api-token \
    --env-file .env/api.dev.env \
    3lpsy/bountydns:latest \
    api-token-create $@


echo "Please use the generated token and save it to the api.dev.env..."
