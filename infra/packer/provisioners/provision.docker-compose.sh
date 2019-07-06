#!/bin/bash

set -e;
export DEBIAN_FRONTEND=noninteractive;

DOCKER_COMPOSE_VERSION="1.24.1"
echo "Provisioning: Docker Compose - Start"

echo "Provisioning: Docker Compose - Downloading Docker Compose"
sudo curl -L https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose


echo "Provisioning: Docker Compose - Marking Docker Compose as Executable"
sudo chmod +x /usr/local/bin/docker-compose

echo "Provisioning: Docker Compose - Complete"