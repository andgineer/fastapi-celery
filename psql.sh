#! /usr/bin/env bash
#
# run psql in postgres container
#
POSTGRES_SERVICE_NAME="postgres"
CREDENTIALS="env/dev-postgres.env"
export $(grep -v '^#' ${CREDENTIALS} | xargs)  # this line should be before we use env vars
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_DB=${POSTGRES_DB}

source container_is_not_running.sh

if container_is_not_running ${POSTGRES_SERVICE_NAME} ; then
    echo
    echo "Postgres container is not running!"
    echo
    echo "Use './up.sh ${POSTGRES_SERVICE_NAME}' to run the container."
    exit
fi

./exec.sh ${POSTGRES_SERVICE_NAME} psql -U $POSTGRES_USER -d $POSTGRES_DB "$@"
