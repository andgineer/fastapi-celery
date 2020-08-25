#! /usr/bin/env bash
#
# Check if the $1 docker-compose service is running for docker-compose env $2
# Default env is empty
#
# Usage:
#   is_container_running postgres
#

function container_is_not_running {
  ENV=${2-""}

  if [[ -z `docker ps -q --no-trunc | grep $(./compose$ENV.sh ps -q $1)` ]]; then
      echo "$1 container from <$ENV> env is not running."
      return 0  # success EXIT code
    else
      return 1
  fi

}
