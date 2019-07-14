#!/bin/bash

set -e;
export DEBIAN_FRONTEND=noninteractive;


echo "Provisioning: BDNS Build - Start"
echo "Provisioning: BDNS Build - Building Compose Project"

cd /opt/bountydns;

echo "Provisioning: BDNS Build - Making /etc/bountydns/env"
sudo mkdir -p /etc/bountydns/env;
sudo touch /etc/bountydns/env/{api,broadcast,db,dns,proxy}.prod.env

echo "Provisioning: BDNS Build - Making /etc/letsencrypt/live/bountydns.proxy.docker"

sudo mkdir -p /etc/letsencrypt/live/bountydns.proxy.docker;

echo "Provisioning: BDNS Build - Building Compose Project"
sudo /opt/bountydns/compose.sh prod build;

echo "Provisioning: BDNS Build - Installing Service File"
sudo cp /opt/bountydns/infra/deploy/services/bountydns-compose.service /etc/systemd/system/bountydns-compose.service;
echo "Provisioning: BDNS Build - Reloading Daemon"
sudo systemctl daemon-reload;

echo "Provisioning: BDNS Build - Complete"