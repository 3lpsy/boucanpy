#!/bin/bash

set -e;

echo "Provisioning: Base - Start"
sudo DEBIAN_FRONTEND=noninteractive apt update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y git apt-transport-https ca-certificates curl software-properties-common

echo "Provisioning: Base - Complete"