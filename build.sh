#! /usr/bin/env bash
# Builds dev version of the container(s)
# Pass all args to docker-compose
#
# Examples:
# build.sh --no-cache backend
# build.sh --no-cache
# build.sh tests
# Function to clean up the .setup-scripts folder
cleanup() {
  rm -rf .setup-scripts
}

# Trap signals and execute the cleanup function
trap cleanup EXIT INT TERM ERR
cp -r ../../docker-scripts .setup-scripts
./compose.sh \
  build \
  "$@"

# Cleanup the .setup-scripts folder (redundant, but ensures cleanup)
cleanup
