#! /usr/bin/env bash
#
# run psql on the host and connects to postgres container
#
POSTGRES_CREDENTIALS="env/dev-postgres.env"

export $(grep -v '^#' ${POSTGRES_CREDENTIALS} | xargs)
PGPASSWORD=$POSTGRES_PASSWORD psql -h 127.0.0.1 -U $POSTGRES_USER
