.PHONY: help dev build test clean docker-up docker-down deploy

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development
dev-backend: ## Start backend development server
	cd backend && uvicorn app.main:app --reload --port 8000

dev-frontend: ## Start frontend development server
	cd frontend && npm run dev

# Installation
install-backend: ## Install backend dependencies
	cd backend && uv pip install -e ".[dev]"

install-frontend: ## Install frontend dependencies
	cd frontend && npm install

install: install-backend install-frontend ## Install all dependencies

# Testing
test-backend: ## Run backend tests with coverage
	cd backend && pytest tests/ -v --cov=app --cov-report=term-missing

test-frontend: ## Run frontend tests
	cd frontend && npm run test

test: test-backend test-frontend ## Run all tests

# Linting
lint-backend: ## Lint backend code
	cd backend && ruff check .
	cd backend && mypy app

lint-frontend: ## Lint frontend code
	cd frontend && npm run lint

lint: lint-backend lint-frontend ## Lint all code

# Docker
docker-build: ## Build Docker images
	docker-compose build

docker-up: ## Start Docker containers
	docker-compose -f docker-compose.dev.yaml up -d

docker-down: ## Stop Docker containers
	docker-compose -f docker-compose.dev.yaml down

docker-logs: ## View Docker logs
	docker-compose -f docker-compose.dev.yaml logs -f

docker-restart: docker-down docker-up ## Restart Docker containers

# Database
db-migrate: ## Run database migrations
	docker-compose -f docker-compose.dev.yaml exec backend alembic upgrade head

db-migration: ## Create new database migration
	docker-compose -f docker-compose.dev.yaml exec backend alembic revision -m "$(MSG)" --autogenerate

db-reset: ## Reset database
	docker-compose -f docker-compose.dev.yaml exec backend alembic downgrade base
	docker-compose -f docker-compose.dev.yaml exec backend alembic upgrade head

# Kubernetes
kube-apply: ## Apply Kubernetes manifests
	kubectl apply -f k8s/

kube-delete: ## Delete Kubernetes resources
	kubectl delete -f k8s/

kube-logs: ## View Kubernetes logs
	kubectl logs -f deployment/backend -n fastapi-vue-app

kube-status: ## View Kubernetes status
	kubectl get all -n fastapi-vue-app

# Cleanup
clean: ## Clean build artifacts
	rm -rf backend/__pycache__ backend/.pytest_cache backend/htmlcov backend/.coverage
	rm -rf frontend/dist frontend/node_modules/.vite
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Production
build: ## Build for production
	cd backend && uv build
	cd frontend && npm run build

deploy: docker-build ## Deploy to production (AKS)
	@echo "Building and pushing Docker images..."
	docker-compose build
	@echo "Applying Kubernetes manifests..."
	kubectl apply -f k8s/