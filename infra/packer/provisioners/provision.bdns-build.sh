#!/bin/bash

set -e;


echo "Provisioning: BDNS Build - Start"
echo "Provisioning: BDNS Build - Building Compose Project"

cd /opt/bountydns;

sudo /opt/bountydns/compose.sh prod pull;

sudo /opt/bountydns/compose.sh prod build;

echo "Provisioning: BDNS Build - Complete"