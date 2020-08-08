#! /usr/bin/env bash
# run tests service with all arguments passed to pytest
#
# Examples:
# test-dev.sh -k enumerate -s
docker-compose \
  -f docker-compose.yml \
  -f docker-compose-dev.yml \
  run --no-deps \
  tests /start.sh \
  "$@"
