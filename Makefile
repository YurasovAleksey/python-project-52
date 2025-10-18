build:
	chmod +x ./build.sh
	./build.sh

install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --noinput

makemigrations:
	uv run python manage.py makemigrations

migrate:
	uv run python manage.py migrate --noinput

render-start:
	gunicorn task_manager.wsgi

run:
	uv run python manage.py runserver

lint:
	uv run ruff check task_manager

lint-fix:
	uv run ruff check --fix task_manager

lint-format:
	uv run ruff format task_manager

test:
	uv run pytest

test-coverage:
	uv run pytest --cov=gendiff --cov-report=xml tests/

check: test lint