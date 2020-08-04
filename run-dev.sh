#! /usr/bin/env bash
# run shell in docker-compose service without deps
# removes container after exit
#
# Examples:
# run-dev.sh tests

docker-compose \
  -f docker-compose.yml \
  -f docker-compose-dev.yml \
  run --no-deps --rm \
  "$@"
