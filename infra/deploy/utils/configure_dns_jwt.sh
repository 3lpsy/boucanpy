#!/bin/bash

## TODO: delete dis

set -eu -o pipefail;

# Try to find the jwtbin binary to generate the jwt token

if [ -x "$(command -v jwtbin)" ]; then
    JWTBIN=$(command -v jwtbin);
elif [[ -d "/usr/local/bin" && -f "/usr/local/bin/jwtbin" ]]; then
    JWTBIN="/usr/local/bin/jwtbin";
elif [[ -d "/opt/bountydns" && -f "/opt/bountydns/infra/deploy/utils/jwtbin" ]]; then
    JWTBIN="/opt/bountydns/infra/deploy/utils/jwtbin";
else
    SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )";
    if [[ -f "$SCRIPTPATH/jwtbin/jwtbin" ]]; then
        JWTBIN="$SCRIPTPATH/jwtbin/jwtbin";
    elif [[ -f "$SCRIPTPATH/jwtbin/jwtbin-linux" ]]; then
        JWTBIN="$SCRIPTPATH/jwtbin/jwtbin-linux";
    else
        echo "Could not find path to 'jwtbin'. Failing.";
        exit 1;
    fi
fi

# We need a source file containing API_SECRET_KEY to generate the jwt
SOURCE_FILE=${1:-/etc/bountydns/env/api.prod.env}
if [[ ! -f "$SOURCE_FILE" ]]; then
    echo "No source file found for $SOURCE_FILE. Failing.";
    exit 1;

fi

# Extract the API_SECRET and rename JWT_SECRET for the jwtbin binary
export JWT_SECRET="$(cat $SOURCE_FILE | grep API_SECRET_KEY | tr -d '\n' | tr -d '\r' | tr -d ' ' | cut -d '=' -f 2-)"
if [[ ${#JWT_SECRET} -lt 10 ]]; then 
    echo "No 'JWT_SECRET' environment variable set. Failing.";
fi

# Generate the jwt token
TOKEN=$($JWTBIN -c 'dns_server_name:default' -c 'sub:1' -c 'scopes:profile dns-request:create dns-request:list zone:list zone:read refresh api-token:syncable' -exp-diff '+72000' -iat-diff '-1000' | tr -d '\n' | tr -d '\r' | tr -d ' ')
unset JWT_SECRET;

# Add the JWT token to the target file using API_TOKEN as the key
TARGET_FILE=${2:-/etc/bountydns/env/dns.prod.env};

if [[ ! -f "$TARGET_FILE" ]]; then
    echo "No target file found for $TARGET_FILE. Failing.";
    exit 1;
fi

echo "Using TARGET_FILE: $TARGET_FILE";
COPY_FILE="/tmp/configure-dns-jwt.copy";
TMP_FILE="/tmp/configure-dns-jwt.tmp";

cp $TARGET_FILE $TMP_FILE

echo "Filtering out previous tokens";
cat $TMP_FILE | grep -v API_TOKEN > $COPY_FILE;
rm $TMP_FILE

echo "Setting TOKEN in Copied Config";
echo "API_TOKEN=$TOKEN" >> $COPY_FILE;

echo "Replacing Config with Modified Copy";
cat "$COPY_FILE" > $TARGET_FILE;
rm $COPY_FILE;
echo "Configure DNS JWT Complete.";
