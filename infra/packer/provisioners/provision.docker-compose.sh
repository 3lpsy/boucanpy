#!/bin/bash

set -e;
DOCKER_COMPOSE_VERSION="1.24.1"
echo "Provisioning: Docker Compose - Start"

sudo curl -L https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo "Provisioning: Docker Compose - Complete"