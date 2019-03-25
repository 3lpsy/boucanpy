#!/bin/bash

if [[ "$1" == 'stop' ]]; then
    docker stop some-postgres
    docker rm some-postgres
else
    docker run --rm --name some-postgres -e POSTGRES_DB=postgrs -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres
fi
