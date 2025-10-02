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
