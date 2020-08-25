#! /usr/bin/env bash
# run tests service with all arguments passed to pytest
#
# Examples:
# test.sh -k token -s
./compose.sh \
  run --no-deps \
  tests /start.sh \
  "$@"
