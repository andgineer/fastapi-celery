#! /usr/bin/env bash
# exec docker-compose service with all arguments
# Pass all args to docker-compose
#
# Examples:
# exec-dev.sh rabbitmq
docker-compose \
  -f docker-compose.yml \
  -f docker-compose-dev.yml \
  exec \
  "$@" \
  bash

