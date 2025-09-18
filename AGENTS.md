# Repository Guidelines

## Project Structure & Module Organization
- `backend/app/`: FastAPI app (`main.py`), Celery (`celery_app.py`), config (`config.py`), API routers (`api/`), DB (`db/`), and tasks (`tasks/`).
- `backend/tests/`: Pytest suite, fixtures, and Celery test setup.
- `docker/`: Service Dockerfiles and dev compose configs; `env/`: local env var files.
- Top-level helpers: `build.sh`, `up.sh`, `run.sh`, `test.sh`, `compose.sh`, `tasks.py` (Invoke tasks).

## Build, Test, and Development Commands
- `./build.sh [service]`: Build images (e.g., `./build.sh backend`).
- `./up.sh [service]`: Start stack or a service; tails logs.
- `./run.sh tests …`: Run a command in the tests container (no deps).
- `./test.sh [pytest-args]`: Run local tests with coverage (e.g., `./test.sh -k token`).
- `invoke pre`: Run pre-commit across the repo; `invoke reqs`: recompile requirements.

## Coding Style & Naming Conventions
- Python 3.x, 4-space indentation, max line length 100 (tests 99).
- Use type hints; keep functions small and log meaningfully.
- Naming: `snake_case` for files/functions, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants.
- Tools: Ruff (lint/format), Mypy (types), Pre-commit. Run `pre-commit run --all-files` before pushing.

## Testing Guidelines
- Framework: Pytest with `celery.contrib.pytest`, FastAPI test client, `fakeredis`.
- Markers: `unittest`, `slow`, `benchmark`, `does_not_change_db` (see `pytest.ini`).
- Naming: `tests/test_*.py`, test functions `test_*`.
- Quick starts: `./test.sh` (parallel), coverage via `--cov` (default includes `backend/app`).
- External server checks: `./up.sh backend` then `./test.sh --host 127.0.0.1`.

## Commit & Pull Request Guidelines
- Commit style: short, imperative summaries; reference issues when relevant (e.g., `fix auth token (#12)` or a URL).
- Include: what/why, screenshots for API docs/UI changes, and linked issues.
- PRs must: pass CI, include tests for new logic, and keep or improve coverage.

## Security & Configuration Tips
- Required env vars (see `backend/app/config.py`): `ADMIN_LOGIN`, `ADMIN_PASSWORD`, `JWT_SECRET_KEY`, `AMQP_*` (host, port, user, password). Do not commit secrets.
- Local dev: map hosts in `/etc/hosts` for `postgres` and `redis`; use `env/*.env` files. Example: `./up.sh postgres` then `./test.sh`.
- Celery/Redis/DB URIs derive from env; validate with startup logs.
