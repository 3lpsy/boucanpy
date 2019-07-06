#!/bin/bash

if [[ "$1" == 'stop' ]]; then
    docker stop postgrs
    docker rm postgres
else
    docker run --rm \
      --name postgres \
      -e POSTGRES_DB=postgrs \
      -e POSTGRES_USER=postgres \
      -e POSTGRES_PASSWORD=postgres \
      -p 127.0.0.1:5432:5432 postgres
fi
