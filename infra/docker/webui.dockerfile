FROM alpine:3.10

RUN mkdir -p /webui

RUN rm -rf /var/cache/apk/* \
    && rm -rf /tmp/*

RUN apk update

RUN apk add --update nodejs npm

# RUN npm install -g typescript
RUN npm install -g @vue/cli

COPY ./webui/package.json /webui/package.json

WORKDIR /webui

RUN npm install

COPY ./webui /webui

COPY ./landing /landing
