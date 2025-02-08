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
migrate:
	docker-compose exec server alembic upgrade head

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