#! /usr/bin/env bash
#
# stops all containers but postgres
#
./compose.sh stop backend celeryworker redis nginx
