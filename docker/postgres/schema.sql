-- autogenerated
-- backend/$ PYTHONPATH=. alembic upgrade head --sql 1> ../docker/postgres/schema.sql 2>/dev/null
-- auto-run on postgres service creation

BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

COMMIT;
