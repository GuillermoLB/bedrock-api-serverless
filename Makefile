.PHONY: up down build test clean logs shell migrate

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

# Clean up
clean:
	docker-compose down -v
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete