#! /usr/bin/env bash
# run docker-compose with an arguments
#
# Examples:
# compose.sh logs tests
cleanup() {
  rm -rf .setup-scripts
}

# Trap signals and execute the cleanup function
trap cleanup EXIT INT TERM ERR
cp -r ../../docker-scripts .setup-scripts

docker-compose \
  -f docker-compose.yml \
  -f docker-compose-dev.yml \
  "$@"

# Cleanup the .setup-scripts folder (redundant, but ensures cleanup)
cleanup
