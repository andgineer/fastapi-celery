#! /usr/bin/env bash
# Builds dev version of the container(s)
# Pass all args to docker-compose
#
# Examples:
# build.sh --no-cache backend
# build.sh --no-cache
# build.sh tests
# Function to clean up the .setup-scripts folder

./compose.sh \
  build \
  "$@"
