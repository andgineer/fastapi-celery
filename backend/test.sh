#! /usr/bin/env bash
# Run pytests and doctests (by unittest) locally
#
# do not forget `. ./activate.sh` before running this script,
# add `127.0.0.1   postgres` into ` /etc/hosts`
# run `docker-compose up -d postgres`
#
# passes params to pytest.
# returned exit code are cumulative of pytest and doctests
#
# Example:
#   ./test.sh -k enumerate

set -o allexport
source ../env/dev-backend.env
source ../env/dev-celeryworker.env
set +o allexport

# run tests with DB settings from .env
POSTGRES_CREDENTIALS="../env/dev-postgres.env"
export $(grep -v '^#' ${POSTGRES_CREDENTIALS} | xargs)

RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color
NL=$'\n'

RUN_DOCTESTS=1
PYTEST_ARGS=""

if [[ "$@" != *"-k"* && "$@" != *"-m"* ]]; then
  PYTEST_ARGS="-n 4"
fi


PY_IGNORE_IMPORTMISMATCH=1 \
  python -m pytest  \
    --instafail \
    --picked=first \
    --cov-report=term-missing:skip-covered \
    --cov-config=../.coveragerc \
    --cov=app \
    -s -vv \
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
    python -m unittest --verbose tests.test_doctests

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
