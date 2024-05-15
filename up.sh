#! /usr/bin/env bash
# Start service(s)
# Pass all params
# Example
#  ./up.sh postgres
./compose.sh \
  up \
  -d \
  "$@"

./compose.sh logs --tail 50 -f "$@"
