#!/bin/bash

if [[ "$1" == "tests" ]]; then
    docker build $(pwd) -f $(pwd)/infra/docker/tests.dockerfile -t bountydns:test
fi
