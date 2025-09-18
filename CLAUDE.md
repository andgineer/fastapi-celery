# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Development Environment Setup
- `./activate.sh` - Activate (and create if needed) Python virtual environment
- `./build.sh` - Build all Docker containers
- `./up.sh` - Start all containers for development
- `./up.sh postgres` - Start only Postgres container (useful for local testing)
- `./up.sh backend` - Start only backend container for testing
- `./stop.sh` - Stop all containers

### Testing
- `./test.sh` - Run all tests locally (requires Postgres container running)
- `./test.sh -k token` - Run tests with 'token' in test name
- `./test.sh -m='unittest and not slow'` - Run fast unit tests only
- `./test.sh -m=benchmark` - Run performance benchmark tests
- `./test.sh --cov` - Run tests with coverage report
- `./test.sh --host 127.0.0.1` - Test against running local server
- `./run.sh tests` - Run tests in Docker container
- `./run.sh tests python -m pytest -v` - Run tests verbosely in container

### Database Operations
- `./alembic.sh revision --autogenerate -m "Schema changes."` - Create migration script
- `./alembic.sh upgrade head` - Apply migrations to database
- `./psql.sh` - Connect to Postgres in Docker container
- `./local-psql.sh` - Connect to local Postgres (requires /etc/hosts entry)

### Code Quality
- `invoke pre` or `inv pre` - Run pre-commit checks (ruff, mypy)
- Pre-commit hooks run ruff with extensive rule set and mypy for type checking

### Requirements Management
- `invoke compile-requirements` or `inv compile-requirements` - Compile .in files to .txt using uv
- `invoke reqs` or `inv reqs` - Upgrade all requirements including pre-commit

## Code Architecture

### Project Structure
- `backend/app/` - Main FastAPI application
  - `main.py` - FastAPI app entry point with middleware setup
  - `config.py` - Configuration management via environment variables
  - `celery_app.py` - Celery worker configuration and task discovery
  - `api/v1/` - API endpoints organized by domain (auth, words, models)
  - `db/` - Database models, session management, and SQLAlchemy setup
  - `tasks/` - Celery task definitions (auto-discovered by celery_app)
  - `controllers/` - Business logic layer

### Technology Stack
- **API Framework**: FastAPI with Gunicorn/Uvicorn
- **Database**: PostgreSQL with SQLAlchemy ORM and Alembic migrations
- **Task Queue**: Celery with Redis broker and backend
- **Proxy**: nginx for load balancing and connection buffering
- **Testing**: pytest with custom markers and fixtures

### Key Configuration
- Environment variables defined in `config.py` under `EnvironmentVarNames`
- Required vars: `ADMIN_LOGIN`, `ADMIN_PASSWORD`, `JWT_SECRET_KEY`, MQ credentials
- Database defaults to localhost Postgres if not specified
- Redis serves as both Celery broker and result backend

### API Structure
- All endpoints prefixed with `/api` (defined in `API_V1_STR`)
- JWT authentication for protected endpoints
- Structured error handling with custom exception handlers
- Database session middleware provides `request.state.db` for each request

### Celery Tasks
- Tasks auto-discovered from `backend/app/tasks/` directory
- Redis connection required for task queuing and results
- Live reload supported in development mode
- Default queue: "main-queue"

### Testing Setup
- Uses `fakeredis` to emulate Redis in tests
- FastAPI test client for API testing
- Custom pytest markers: `unittest`, `slow`, `benchmark`, `does_not_change_db`
- Separate test requirements in `docker/tests/requirements.txt`

### Docker Development
- Development mode uses live reload for both FastAPI and Celery
- Volumes mounted for hot reloading in dev environment
- Production mode uses Gunicorn with multiple workers
- nginx proxy on port 8001, backend on port 80

### Local Development
- Add to `/etc/hosts`: `127.0.0.1 postgres` and `127.0.0.1 redis`
- Allows running backend/celery locally while connecting to containerized services
- Useful for debugging with IDE integration
