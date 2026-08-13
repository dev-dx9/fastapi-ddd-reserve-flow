default:
    just --list

run:
    uv run uvicorn src.main:app --reload

format:
    uv run ruff format .

format-check:
    uv run ruff format --check .

lint:
    uv run ruff check .

typecheck:
    uv run pyright

test:
    uv run pytest

check: format-check lint typecheck test

migrate:
    uv run alembic upgrade head

migration-check:
    uv run alembic check

revision name:
    uv run alembic revision --autogenerate -m "{{name}}"

psql:
    docker compose exec postgres \
        psql -U postgres -d reserve_flow