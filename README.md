# Python backend: FastAPI + SQLAlchemy/Postgres + Celery/Redis

Application template to quick start your API server.

Fully Dockerized local development environment.

## Installation

### Activate (and/or create) the Python environment 

```
. ./activate.sh
```

## Local development

### Build and run all containers

```console
./up-dev.sh 
```

You can debug backend and celery tasks code locally - it will connect to postgres and rabbitmq 
in containers.

## Working with DB

See docker/postgres/README.md.

### Create migration script

```console
# compare DB models and current DB and create DB upgrade script in alembic/versions
./alembic-dev.sh revision --autogenerate -m "Schema changes."

# apply script to the DB so after that DB meta data will reflect DB models  
./alembic-dev.sh upgrade head
```

## Testing

You only need Posgtres to run test container.
We use fake redis to emulate Redis, fastapi test client to emulate fastapi server.

For DB we use `fixtures/db` that wrap and roll back all test transactions leaving DB 
intact after each test.

```console
./up-dev.sh -d postgres
```

### Run tests from container

```console
./run-dev.sh tests  # run all tests
./run-dev.sh tests python -m pytest -v  # run tests `verbosely`
```

### Run tests locally (as unit-tests without server running)

in `/etc/hosts` we need

    127.0.0.1   postgres

in folder `/backend` execute

```console
./test.sh -k enumerate  # run tests with `enumerate` in test name
./test.sh -m='unittest and not slow'  # run all fast unittests (locally)
./test.sh -m=benchmark  # run all tests that mesures speed using pytest-benchmark
./test.sh --markers  # see all markers that we can user in `-m`
./test.sh --cov  # run tests with coverage report
```

### Test local server

```console
./up-dev.sh -d backend
./test.sh --host 127.0.0.1 
```

This command run local server and test it.
It will skip unit tests that cannot be run for external server (marked as `unittest`).
