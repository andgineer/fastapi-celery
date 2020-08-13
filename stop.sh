#! /usr/bin/env bash
#
# stops all containers but postgres
#
./docker-dev.sh stop backend celeryworker redis nginx
