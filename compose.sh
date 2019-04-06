#!/bin/bash

set -e;

env="${1}"
shift ;
if [[ ${#env} -lt 3 ]]; then
    echo "please pass the environment type: compose.sh [env] [args]"
elif [[ "${env}" == "dev" ]]; then
    export COMPOSE_PATH_SEPARATOR=:
    export COMPOSE_FILE=docker-compose.dev.build.yml:docker-compose.dev.env.yml:docker-compose.dev.ports.yml:docker-compose.dev.command.yml:docker-compose.dev.restart.yml:docker-compose.dev.networks.yml:docker-compose.dev.depends.yml:docker-compose.dev.volumes.yml
else
    echo "please pass a valid environment type: compose.sh [env] [args]"
fi

cd infra/compose
docker-compose $@;
