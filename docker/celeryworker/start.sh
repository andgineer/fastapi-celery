#! /usr/bin/env bash
set -e

#python /app/app/celeryworker_pre_start.py
export PYTHONPATH="/"

# wait for rabbitmq
while ! nc -z rabbitmq 5672; do sleep 3; done

if [ $env == 'dev' ] ; then
  # celery 4 does not support auto-reload so we use watchdog to reload celery on tasks changes
  watchmedo \
    auto-restart \
    --directory=./app/tasks/ \
    --pattern=*.py \
    --recursive \
    -- \
    celery worker -A app.celery_app \
    -l info \
    -Q main-queue \
    -c 1 \
    -O fair \
    --heartbeat-interval 10 \
    --statedb=/var/run/celery/%n.state
else
  celery worker -A app.celery_app \
    -l info \
    -Q main-queue \
    -c 1 \
    -O fair \
    --heartbeat-interval 10 \
    --statedb=/var/run/celery/%n.state
fi

# -O fair to disable rabbitmq prefetching behavior
# statedb to store revoke (kill task) info persistently and do not loose it on worker restart
