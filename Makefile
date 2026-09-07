.PHONY: install test lint typecheck quality run docker-build up down logs clean

install:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements-dev.txt

test:
	.venv/bin/pytest -v

lint:
	.venv/bin/ruff check .

typecheck:
	.venv/bin/mypy app wsgi.py

quality: lint typecheck

run:
	FLASK_APP=wsgi.py .venv/bin/flask run --port 5001

docker-build:
	docker compose build

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

clean:
	rm -rf .venv .pytest_cache .ruff_cache .mypy_cache **/__pycache__ report.xml
