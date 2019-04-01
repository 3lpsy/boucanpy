FROM node:alpine

RUN mkdir -p /webui

# RUN npm install -g typescript
RUN npm install -g @vue/cli

COPY ./webui/package.json /webui/package.json

WORKDIR /webui

RUN npm install

COPY ./webui /webui

COPY ./web /web
