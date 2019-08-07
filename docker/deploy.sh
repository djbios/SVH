#!/usr/bin/env bash
# On clean machine install:
# sudo apt install git
# curl -fsSL https://get.docker.com -o get-docker.sh
# sudo sh get-docker.sh
# sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
# sudo chmod +x /usr/local/bin/docker-compose
# git clone https://github.com/djbios/SVH
cd "$(dirname "$0")"

: ${SVH_SOURCES:=/www/svh/sources}

docker-compose -p svh build --pull
docker-compose -p svh up -d --remove-orphans