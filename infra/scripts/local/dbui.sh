#!/bin/bash

if [[ "$1" == 'stop' ]]; then
    docker stop pgadmin
    docker rm pgadmin
else
    docker run --rm --name pgadmin \
    -e PGADMIN_DEFAULT_EMAIL=admin \
    -e PGADMIN_DEFAULT_PASSWORD=password \
    -e POSTGRES_DB=postgrs \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e PGADMIN_LISTEN_PORT=5000 \
    -p 127.0.0.1:5000:5000 \
    --link postgres:postgres dpage/pgadmin4
fi
