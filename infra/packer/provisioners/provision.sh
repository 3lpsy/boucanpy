#!/bin/bash

set -e;

echo "Provisioning: Base - Start"
echo "Provisioning: Base - Updating Repos"
sudo DEBIAN_FRONTEND=noninteractive apt update

echo "Provisioning: Base - Installing Base Packages"
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y git apt-transport-https ca-certificates curl software-properties-common

echo "Provisioning: Base - Complete"