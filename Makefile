.PHONY: install test run docker-build up down logs clean

install:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

test:
	.venv/bin/pytest -v

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
	rm -rf .venv .pytest_cache **/__pycache__ report.xml
