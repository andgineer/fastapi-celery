#! /usr/bin/env bash
# exec docker-compose service with all arguments
# Pass all args to docker-compose
#
# Examples:
# exec.sh rabbitmq
./compose.sh \
  exec \
  "$@" \
  bash
