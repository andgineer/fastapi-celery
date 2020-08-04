#! /usr/bin/env bash
# Builds dev version of the container(s)
# Pass all args to docker-compose
#
# Examples:
# build-dev.sh --no-cache backend
# build-dev.sh --no-cache
# build-dev.sh tests

docker-compose \
  -f docker-compose.yml \
  -f docker-compose-dev.yml \
  build \
  "$@"
