#! /usr/bin/env bash
test_it () { python -m pytest tests -n 2 --host=127.0.0.1 "$@"; }

until ! test_it "$@"; do
  echo "------------------$?"
done
