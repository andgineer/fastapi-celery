#! /usr/bin/env bash
#
# Fast API test for external server
# Usage:
# smoke_test.sh <server name>
#    supported server names
#       local - local server
#       dev - dev server
#

if [[ -z $1 ]]; then
  echo "Select server to test:"
  select SERVER in local dev; do
    break
  done
fi
case $SERVER in
     local)
          HEADER=""
          HOST="127.0.0.1"
          ;;
     dev)
          HEADER="Host: ???"
          HOST="???"
          ;;
esac

echo "Test server $HOST with $HEADER"

curl -D- \
  -X GET \
  -H "Content-Type: application/json" \
  --header "$HEADER" \
  --insecure \
  ${HOST}/api/
