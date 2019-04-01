FROM python:3.7-alpine3.9

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
