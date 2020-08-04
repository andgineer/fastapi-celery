#! /usr/bin/env bash
# Start service(s)
# Pass all params
# Example
#  ./up-dev.sh -d postgres
docker-compose \
  -f docker-compose.yml \
  -f docker-compose-dev.yml \
  up --build \
  "$@"
