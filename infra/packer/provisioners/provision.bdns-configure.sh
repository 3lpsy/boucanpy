#!/bin/bash

set -e;


echo "Provisioning: BDNS Configure - Start"
echo "Provisioning: BDNS Configure - Making /etc/bountydns/env"

sudo mkdir -p /etc/bountydns/env;

sudo touch /etc/bountydns/env/{api,broadcast,db,dns,proxy}.prod.env

sudo cp /opt/bountydns/infra/deploy/bountydns-compose.service /etc/systemd/system/bountydns-compose.service;

sudo systemctl daemon-reload;

echo "Provisioning: BDNS Configure - Complete"