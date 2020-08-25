#! /usr/bin/env bash
# run shell in docker-compose service without deps
# removes container after exit
#
# Examples:
# run.sh tests

./compose.sh \
  run --no-deps --rm \
  "$@"
