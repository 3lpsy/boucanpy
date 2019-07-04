#!/bin/bash

set -e;

SUDOER="ubuntu"

echo "Provisioning: Docker - Start"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt update
sudo apt-cache policy docker-ce
sudo apt install -y docker-ce
sudo systemctl status docker
sudo systemctl enable docker

sudo usermod -aG docker ${SUDOER}

echo "Provisioning: Docker - Complete"