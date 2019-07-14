#!/bin/bash

set -e;

export COMPOSE_PROJECT_NAME=bountydns
compose="docker-compose"

env="${1}"

shift ;

if [[ ${#env} -lt 3 ]]; then
    echo "please pass the environment type: compose.sh [env] [args]"
elif [[ "${env}" == "dev" ]]; then
    export COMPOSE_ENV_DIR="$PWD/.env"
    export COMPOSE_PATH_SEPARATOR=:
    export COMPOSE_FILE=docker-compose.dev.build.yml:docker-compose.dev.ports.yml:docker-compose.dev.volumes.yml
elif [[ "${env}" == "prod" ]]; then
    if [[ -d "/etc/bountydns/env" ]]; then
        export COMPOSE_ENV_DIR="/etc/bountydns/env"
    else
        export COMPOSE_ENV_DIR="$PWD/.env"
    fi

    if [[ -d "/etc/letsencrypt/live" ]]; then
        export TLS_HOST_DIR="/etc/letsencrypt/live";
    else
        export TLS_HOST_DIR="$PWD/.tls";
    fi 
    if [[ ! -d ${TLS_HOST_DIR}/bountydns.proxy.docker ]]; then 
        mkdir ${TLS_HOST_DIR}/bountydns.proxy.docker;
    fi
    compose="$compose -f docker-compose.prod.yml"
else
    echo "please pass a valid environment type: compose.sh [env] [args]"
fi

cd $PWD/infra/compose

$compose $@;
