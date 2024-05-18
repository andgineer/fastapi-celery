[![Build Status](https://github.com/andgineer/fastapi-celery/workflows/ci/badge.svg)](https://github.com/andgineer/fastapi-celery/actions)
# Python backend: FastAPI/Gunicorn + SQLAlchemy/Postgres + Celery/Redis + nginx

Application template to quick start your API server.

Fully Dockerized local development environment.

In dev mode (`$env=dev``) uses `uvicorn` with live-reload (sources mounted to the
container). And Celery worker with live reload.

## Installation

### Activate (and/or create) the Python environment

```
. ./activate.sh
```

## Local development

### Build and run all containers

```console
./build.sh
./up.sh
```

### Sanity check with hurl

Install [hurl](https://hurl.dev/)

    hurl docker/words.hurl

That will get auth tocket from backend running in the Docker, send `words` request to API and check response
(it should be number of words in file `docker/words.txt`).

### Local debug

You can debug backend and celery tasks code locally, outside containers.
Backend and Celery worker will connect to Postgres and Redis in containers.
For that you need in your `/etc/hosts`:

    127.0.0.1   postgres
    127.0.0.1   redis

## Working with DB

See docker/postgres/README.md.

### Create migration script

```console
# compare DB models and current DB and create DB upgrade script in alembic/versions
./alembic.sh revision --autogenerate -m "Schema changes."

# apply script to the DB so after that DB meta data will reflect DB models
./alembic.sh upgrade head
```

## Testing

You only need `Posgtres` to run test container.
We use `fakeredis` to emulate `Redis`, `fastapi` `test client` to emulate fastapi server.

```console
./up.sh postgres
```

### Run tests from container

```console
./run.sh tests  # run all tests
./run.sh tests python -m pytest -v  # run tests `verbosely`
```

### Run tests locally (as unit-tests without server running)

in `/etc/hosts` we need

    127.0.0.1   postgres

in folder `/backend` execute

```console
./test.sh -k token  # run tests with `token` in test name
./test.sh -m='unittest and not slow'  # run all fast unittests (locally)
./test.sh -m=benchmark  # run all tests that mesures speed using pytest-benchmark
./test.sh --markers  # see all markers that we can use with `-m` key
./test.sh --cov  # run tests with coverage report
```

### Test local server

```console
./up.sh backend
./test.sh --host 127.0.0.1
```

This command run local server and test it.
It will skip unit tests that cannot be run for external server (marked as `unittest`).

### Stress test

Run tests in parallel in loop as some kind of stress-test using nginx as proxy.

In folder `backend/` run:
```console
./stress.sh
```

## Swagger / OpenAPI

Swagger UI available at `localhost/docs` after server start (`./up.sh`).

# nginx proxy

Nginx proxy at `8001` port.

Without nginx gunicorn server will drop a lot of incoming connections.
Because there are only `<CPU number> + 1` workers in production mode.
Or even only one worker in live reload (`$env=dev`) mode.

Nginx will buffer requests so your server will serve a lot of parallel clients.
