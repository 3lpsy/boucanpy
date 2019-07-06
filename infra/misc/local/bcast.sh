#!/bin/bash


docker run --rm -e REDIS_PASSWORD=redis -p 127.0.0.1:6379:6379 --name redis bitnami/redis:latest

if [[ "$1" == 'stop' ]]; then
    docker stop redis
    docker rm redis
else
    docker run --rm -e REDIS_PASSWORD=redis -p 127.0.0.1:6379:6379 --name redis bitnami/redis:latest
fi
