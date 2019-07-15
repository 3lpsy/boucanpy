#!/bin/bash

set -e;

echo "Provisioning: Base - Start"
echo "Provisioning: Base - Updating Repos"
export DEBIAN_FRONTEND=noninteractive;

sudo DEBIAN_FRONTEND=noninteractive apt-get clean
sudo DEBIAN_FRONTEND=noninteractive apt update

echo "Provisioning: Base - Installing Base Packages"
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y git apt-transport-https ca-certificates curl software-properties-common

sudo hostnamectl set-hostname bdns
echo -n "bdns" | sudo tee /etc/hostname;
echo "127.0.0.1 bdns" | sudo tee -a /etc/hosts
sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved
sudo rm /etc/resolv.conf

echo "nameserver 1.1.1.1" | sudo tee /etc/resolv.conf
echo "Provisioning: Base - Complete"