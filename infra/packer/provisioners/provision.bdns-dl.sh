#!/bin/bash

set -e;


echo "Provisioning: BDNS Download - Start"
echo "Provisioning: BDNS Download - Cloning BountyDNS to /opt/bountydns"

sudo git clone https://github.com/3lpsy/bountydns.git /opt/bountydns

echo "Provisioning: BDNS Download - Complete"