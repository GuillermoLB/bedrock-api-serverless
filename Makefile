.PHONY: up down build test clean logs shell migrate test-local test-local-v test-local-cov coverage-report

set_path:
	export PYTHONPATH=$(pwd)/app

libs:
	@echo "Installing libraries..."
	pip install --upgrade pip
	pip install --progress-bar on --no-cache-dir -r requirements_dev.txt

stop_postgres_service:
	sudo systemctl stop postgresql

# Docker commands
up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

logs:
	docker-compose logs -f

shell:
	docker-compose exec server /bin/bash

# Database
db:
	docker-compose up -d db

migrate:
	docker-compose exec server alembic upgrade head

# Local development
local:
	make db
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Testing
test:
	docker-compose exec server pytest

test-v:
	docker-compose exec server pytest -v

test-cov:
	docker-compose exec server pytest --cov=app --cov-report=term-missing

# Local testing (without Docker)
test-local:
	python -m pytest app/tests

# Local testing with verbose output
test-local-v:
	python -m pytest app/tests -v

# Local testing with coverage
test-local-cov:
	python -m pytest app/tests --cov=app --cov-report=term-missing --cov-report=html

# Open the coverage report in the browser
coverage-report:
	open htmlcov/index.html

# Clean up
clean:
	docker-compose down -v
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete