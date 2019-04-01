#!/bin/bash

set -e;
echo "[*] Must be run from root project directory";

# TODO: make context and dockerfile dynamic
function build_api() {
    BDOCKERFILE=$(pwd)/infra/docker/bountydns.dockerfile
    BCONTEXT="$(pwd)"
    docker build -f $BDOCKERFILE $BCONTEXT -t 3lpsy/bountydns:latest;
}

function build_webui() {
    WDOCKERFILE=$(pwd)/infra/docker/webui.dockerfile
    WCONTEXT="$(pwd)/bountydns"
    docker build -f $WDOCKERFILE $WCONTEXT -t 3lpsy/bountydns-webui:latest;
}

function build_proxy() {
    NDOCKERFILE=$(pwd)/infra/docker/nginx.dockerfile
    NCONTEXT="$(pwd)/infra/nginx"
    docker build -f $NDOCKERFILE $NCONTEXT -t 3lpsy/bountydns-proxy:latest;
}

if [[ ${#1} -lt 2 ]]; then
    build_api
    build_webui
    build_proxy
else
    build_$1
fi
