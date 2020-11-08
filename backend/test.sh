#! /usr/bin/env bash
# local test
# do not forget `. ./activate.sh`
# In /etc/hosts you need 127.0.0.1   postgres
#
# passes params to pytest
# Example:
#   ./test.sh -k enumerate

# run tests with DB settings from .env
POSTGRES_CREDENTIALS="../env/dev-postgres.env"
export $(grep -v '^#' ${POSTGRES_CREDENTIALS} | xargs)

RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color
NL=$'\n'

RUN_DOCTESTS=0
PYTEST_ARGS=""

if [[ "$@" != *"-k"* && "$@" != *"-m"* ]]; then
  # full test suit
  RUN_DOCTESTS=1
  PYTEST_ARGS="-n 4"
fi

if [[ "$@" == *"--host"* ]]; then
  # test external server
  RUN_DOCTESTS=0
#  PYTEST_ARGS=""
fi


PY_IGNORE_IMPORTMISMATCH=1 \
  python -m pytest  \
    --instafail \
    --picked=first \
    -s -vv --no-hints \
    $PYTEST_ARGS \
    "$@"

if [ $? -eq 0 ]; then
  echo
  echo -e $GREEN".. pytest success .."$NC
  EXIT_CODE=0
else
  echo
  echo -e $RED".. pytest FAIL!"$NC
  EXIT_CODE=1
fi

if [[ $RUN_DOCTESTS == 1 ]]; then
    python -m unittest --verbose

    if [ $? -eq 0 ]; then
      echo
      echo -e $GREEN".. doctests success .."$NC
      EXIT_CODE=$((0 || $EXIT_CODE))
    else
      echo
      echo -e $RED"doctests FAIL!"$NC
      EXIT_CODE=1
    fi
    echo
fi

exit $EXIT_CODE
