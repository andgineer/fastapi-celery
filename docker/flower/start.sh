#! /usr/bin/env bash
set -e
flower --loglevel=info --broker=amqp://rabbitmq:5672
