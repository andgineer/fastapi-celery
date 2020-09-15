#! /usr/bin/env bash

python -m pytest -s -vv --no-hints tests/ "$@"
