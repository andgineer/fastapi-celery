#! /usr/bin/env bash
# run docker-compose with an arguments
#
# Examples:
# docker-dev.sh logs tests
docker-compose \
  -f docker-compose.yml \
  -f docker-compose-dev.yml \
  "$@"
