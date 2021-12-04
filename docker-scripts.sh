#!/bin/bash

apt-get update
apt-get install -y --no-install-recommends git python3-pip
apt-get install -y gcc
rm -rf /var/lib/apt/lists/*