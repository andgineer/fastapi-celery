#! /usr/bin/env bash
# exec or run alembic in backend container
# Pass all args to it
#
# Usage:
#   alembic-dev.sh history

SERVICE_NAME="backend"

source container_is_not_running.sh
args="$@"

if container_is_not_running ${SERVICE_NAME} ; then
  echo "Using RUN instead of EXEC"
  ./run-dev.sh \
    ${SERVICE_NAME} \
    bash -c \
    "PYTHONPATH=. alembic $args"
else
  ./docker-dev.sh \
    exec \
    ${SERVICE_NAME} \
    bash -c \
    "PYTHONPATH=. alembic $args"
fi