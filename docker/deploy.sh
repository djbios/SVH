#!/usr/bin/env bash
docker-compose -p svh build --pull
docker-compose -p svh up -d --remove-orphans