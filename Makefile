.PHONY: help lint format check fix clean run dev test test-cov \
	docker-up docker-down docker-logs docker-test docker-test-cov \
	docker-prod-up docker-prod-down docker-prod-logs

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

lint: ## Run linting checks with ruff
	uv run ruff check .

format: ## Format code with ruff
	uv run ruff format .

check: ## Run linting and format checks
	uv run ruff check .
	uv run ruff format --check .

fix: ## Fix linting issues and format code
	uv run ruff check --fix .
	uv run ruff format .

clean: ## Clean ruff cache
	uv run ruff clean

test: ## Run test suite
	uv run pytest tests/ -v

test-cov: ## Run test suite with coverage
	uv run pytest tests/ --cov=app --cov-report=html --cov-report=term

run: ## Run the application
	uv run python run.py

dev: ## Run the application in development mode with auto-reload
	uv run uvicorn app.main:app --reload

docker-up: ## Start Docker containers for development
	docker compose up -d

docker-down: ## Stop Docker containers
	docker compose down

docker-logs: ## View Docker container logs
	docker compose logs -f

docker-test: ## Run tests in Docker container
	docker compose exec app uv run pytest tests/ -v

docker-test-cov: ## Run tests with coverage in Docker container
	docker compose exec app uv run pytest tests/ --cov=app --cov-report=html --cov-report=term

docker-prod-up: ## Build and start Docker containers for production
	docker compose -f docker-compose.prod.yml up -d --build

docker-prod-down: ## Stop production Docker containers
	docker compose -f docker-compose.prod.yml down

docker-prod-logs: ## View production Docker container logs
	docker compose -f docker-compose.prod.yml logs -f
