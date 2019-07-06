#!/bin/bash

echo "Provisioning: JWTBin - Start"

sudo wget https://github.com/3lpsy/jwtbin/releases/download/v0.1.1/jwtbin-linux-amd64 -O /usr/local/bin/jwtbin;

sudo chmod +x /usr/local/bin/jwtbin

echo "Provisioning: JWTBin - Complete"
