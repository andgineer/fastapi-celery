#! /usr/bin/env bash
set -e

MODULE_NAME=${MODULE_NAME:-app.main}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-80}
LOG_LEVEL=${LOG_LEVEL:-info}

# If there's a prestart.sh script in the /app directory, run it before starting
PRE_START_PATH=/app/prestart.sh
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    . "$PRE_START_PATH"
else
    echo "There is no script $PRE_START_PATH"
fi

# wait for redis
#sleep 1

if [ $env == 'dev' ] ; then
  echo "!!!DEBUG MODE!!! Start Uvicorn with live reload"
  exec uvicorn \
    --host $HOST --port $PORT \
    --log-level debug \
    --reload \
    --reload-dir /backend/app \
    "$APP_MODULE"
else
  echo "Start gunicorn in production mode"
  if [ -f /app/gunicorn_conf.py ]; then
      DEFAULT_GUNICORN_CONF=/app/gunicorn_conf.py
  else
      DEFAULT_GUNICORN_CONF=/gunicorn_conf.py
  fi
  export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}

  exec gunicorn -k uvicorn.workers.UvicornWorker -c "$GUNICORN_CONF" "$APP_MODULE"
fi
