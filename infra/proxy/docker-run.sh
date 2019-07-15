#!/bin/bash

set -e;

if [[ "$SSL_ENABLED" == "1" ]]; then
    PREFIX="ssl";
else
    PREFIX="insecure"
fi

echo "Using conf: ${PREFIX}.nginx.conf"

cp /nginxconfs/${PREFIX}.nginx.conf /etc/nginx/nginx.conf

if [[ ${#API_BACKEND_PROTO} -lt 2 ]]; then
    API_BACKEND_PROTO="http";
fi


if [[ ${#API_BACKEND_HOST} -lt 2 ]]; then
    API_BACKEND_HOST="127.0.0.1";
fi

if [[ ${#API_BACKEND_PORT} -lt 2 ]]; then
    API_BACKEND_PORT="8080";
fi

echo "Using API : ${API_BACKEND_PROTO}://${API_BACKEND_HOST}:${API_BACKEND_PORT}"

sed -i "s/API_BACKEND_PROTO/$API_BACKEND_PROTO/g" /etc/nginx/nginx.conf
sed -i "s/API_BACKEND_HOST/$API_BACKEND_HOST/g" /etc/nginx/nginx.conf
sed -i "s/API_BACKEND_PORT/$API_BACKEND_PORT/g" /etc/nginx/nginx.conf
sed -i "s/INSECURE_LISTEN_PORT/$INSECURE_LISTEN_PORT/g" /etc/nginx/nginx.conf
sed -i "s/SECURE_LISTEN_PORT/$SECURE_LISTEN_PORT/g" /etc/nginx/nginx.conf
sed -i "s#TLS_DIR#$TLS_DIR#g" /etc/nginx/nginx.conf

if [[ "$DEBUG_CONF" == "1" ]]; then
    cat /etc/nginx/nginx.conf;
fi

exec nginx -g "daemon off;";
