#! /usr/bin/env bash

ENV_NAME="fastapi-celery"

RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color

if ! (return 0 2>/dev/null) ; then
    # If return is used in the top-level scope of a non-sourced script,
    # an error message is emitted, and the exit code is set to 1
    echo
    echo -e $RED"This script should be sourced like"$NC
    echo "    . ./activate.sh"
    echo
    exit 1  # we detected we are NOT source'd so we can use exit
fi

if type conda 2>/dev/null; then
    if conda info --envs | grep "\b${ENV_NAME}\s"; then
      echo -e $CYAN"activating environment ${ENV_NAME}"$NC
    else
      if [[ -z $(conda list --name base | grep mamba) ]]; then
        echo "..installing mamba.."
        conda install mamba --name base -c conda-forge
      fi
      echo -e $CYAN"creating conda environment ${ENV_NAME}"$NC
      conda create -y --name ${ENV_NAME} python=3.12
      conda activate ${ENV_NAME}
      conda install -y pip
      pip install -r docker/backend/requirements.txt
      pip install -r docker/celeryworker/requirements.txt
      pip install -r docker/tests/requirements.txt
      conda deactivate  # RE-activate conda env so python will have access to conda installed deps
    fi
else
    echo
    echo -e $RED"(!) Please install anaconda"$NC
    echo
    return 1  # we are source'd so we cannot use exit
fi

conda activate ${ENV_NAME}
