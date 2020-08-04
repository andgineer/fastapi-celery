## Migrate DB to the latest version

To create all tables and other object in DB 

```console
./alembic-dev.sh upgrade head
```

That will execute all alembic scripts from `alembic/versions`.

## Generation of `schema.sql`

The `schema.sql` executed when Docker creates new DB in `postgres`
container.

To create the file go into folder `backend` and execute:
```bash
PYTHONPATH=. alembic upgrade head --sql 1> ../docker/postgres/schema.sql 2>/dev/null
```

If you have not installed Alembic locally you can run it from
`backend` container:
```console
./alembic-dev.sh upgrade head --sql 1> ../docker/postgres/schema.sql 2>/dev/null
```

## Load small test data to database

After creating postgres container (it will be init with `schema.sql`)
```console
./upsert-dev.sh
```

