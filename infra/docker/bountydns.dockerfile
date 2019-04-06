FROM python:3.7-alpine3.9

## API Server Variables
ENV API_ENV=dev
ENV API_SECRET_KEY=helloworld
ENV API_SERVER_NAME=boutydns
ENV API_SERVER_HOST=127.0.0.1:8080
ENV API_CORS_ORIGINS=http://127.0.0.1:8080,http://localhost:8080
ENV DB_DRIVER=postgresql
ENV DB_HOST=db
ENV DB_PORT=5432
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres
ENV DB_DATABASE=postgres
ENV BROADCAST_ENABLED=1
ENV BROADCAST_DRIVER=redis
ENV BROADCAST_HOST=broadcast
ENV BROADCAST_PORT=6379
ENV BROADCAST_PASSWORD=redis
ENV BROADCAST_PATH=0
ENV SEED_USER_0_EMAIL=jim@jim.jim
ENV SEED_USER_0_PASSWORD=password123
ENV SEED_USER_0_SUPERUSER=1

## DNS Server Variables
# API_URL=http://proxy:8080
# API_TOKEN

# TODO: don't run as root

COPY ./requirements.txt /requirements.txt

# install pip modules with build time dependencies
# TODO: remove alpine-sdk for smaller size (install make?)
RUN apk update \
    && apk add --virtual build-deps gcc alpine-sdk python3-dev musl-dev libffi-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && pip install -U setuptools pip \
    && pip install --no-cache-dir -r  /requirements.txt  \
    && apk del build-deps

COPY ./docker-run.sh /usr/bin/docker-run.sh
RUN chmod +x /usr/bin/docker-run.sh

COPY . /bountydns
WORKDIR /bountydns

EXPOSE 8080

ENTRYPOINT ["/usr/bin/docker-run.sh"]
