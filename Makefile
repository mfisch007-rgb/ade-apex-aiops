.PHONY: help install dev lint format test test-unit test-integration test-e2e clean run docker-up docker-down

help:
	@echo "ADE-APEX Development Commands"
	@echo ""
	@echo "install            Install dependencies"
	@echo "dev                Start development server"
	@echo "run                Run application"
	@echo "lint               Run linting"
	@echo "format             Format code"
	@echo "test               Run all tests"
	@echo "test-unit          Run unit tests"
	@echo "test-integration   Run integration tests"
	@echo "test-e2e           Run end-to-end tests"
	@echo "docker-up          Start Docker services"
	@echo "docker-down        Stop Docker services"
	@echo "clean              Remove caches"

install:
	pip install -e ".[dev]"

dev:
	uvicorn app.main:app --reload

run:
	uvicorn app.main:app

lint:
	ruff check app tests

format:
	ruff format app tests

test:
	pytest

test-unit:
	pytest tests/unit

test-integration:
	pytest tests/integration

test-e2e:
	pytest tests/e2e

docker-up:
	docker compose up -d

docker-down:
	docker compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
