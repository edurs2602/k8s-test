# CI/CD Documentation

This document describes the CI/CD pipelines for this project.

## GitHub Actions

Located at `.github/workflows/ci-cd.yaml`

### Workflow Triggers

- **Push**: `main`, `develop` branches
- **Pull Request**: `main`, `develop` branches

### Workflow Jobs

| Job | Description | Runs On |
|-----|-------------|---------|
| `backend-test` | Lint, type-check, and test backend | ubuntu-latest |
| `frontend-test` | Lint, type-check, build frontend | ubuntu-latest |
| `build-images` | Build Docker images (main only) | ubuntu-latest |
| `deploy` | Deploy to AKS (main only) | ubuntu-latest |

### Required Secrets

| Secret | Description |
|--------|-------------|
| `AZURE_CLIENT_ID` | Azure Service Principal Client ID |
| `AZURE_CLIENT_SECRET` | Azure Service Principal Secret |
| `AZURE_TENANT_ID` | Azure Tenant ID |
| `AZURE_SUBSCRIPTION_ID` | Azure Subscription ID |
| `AZURE_RESOURCE_GROUP` | AKS Resource Group |
| `AKS_CLUSTER_NAME` | AKS Cluster Name |
| `GITHUB_TOKEN` | GitHub Token (auto-provided) |

### Setup GitHub Actions

1. Go to Repository > Settings > Secrets and variables > Actions
2. Add each required secret
3. Create an Azure Service Principal with contributor access:
   ```bash
   az ad sp create-for-rbac --name "github-actions" \
     --role contributor \
     --scopes /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP> \
     --sdk-auth
   ```

---

## GitLab CI/CD

Located at `.gitlab-ci.yml`

### Pipeline Stages

| Stage | Jobs |
|-------|------|
| `test` | `backend-test`, `frontend-test` |
| `build` | `build-backend`, `build-frontend` |
| `deploy` | `deploy-develop`, `deploy-production` |

### Required Variables

| Variable | Description |
|----------|-------------|
| `CI_REGISTRY` | Container registry URL |
| `CI_REGISTRY_USER` | Registry username |
| `CI_REGISTRY_PASSWORD` | Registry password |
| `KUBE_CONTEXT_DEV` | Kubernetes context for dev |
| `KUBE_CONTEXT_PROD` | Kubernetes context for prod |

### GitLab Runner Configuration

Configure runners in: **Settings > CI/CD > Runners**

```yaml
# Example runner tags
.using-docker-runner:
  tags:
    - docker
    - linux

.using-kubernetes-runner:
  tags:
    - kubernetes
    - production
```

---

## Local Testing

### Backend

```bash
cd backend

# Install dependencies
uv pip install -e ".[dev]"

# Run linting
ruff check .

# Run type checking
mypy app

# Run tests with coverage
pytest tests/ -v --cov=app --cov-report=html

# Run specific test
pytest tests/test_items.py -v
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run linting
npm run lint

# Run type checking
npm run type-check

# Run tests
npm run test

# Run tests with coverage
npm run test:coverage

# Build for production
npm run build
```

---

## Docker Build

### Backend

```bash
docker build -t backend:latest ./backend
```

### Frontend

```bash
docker build -t frontend:latest ./frontend
```

### Docker Compose

```bash
# Development
docker-compose -f docker-compose.dev.yaml up -d

# Production
docker-compose up -d
```

---

## Deployment

### AKS Deployment Steps

1. **Push to main branch** triggers deployment
2. **Images are built** and pushed to GitHub Container Registry
3. **Manifests are applied** to AKS cluster
4. **Rollout is monitored** for success

### Manual Deployment

```bash
# Set AKS context
az aks get-credentials --resource-group <RG> --name <CLUSTER>

# Update image tags
sed -i "s|:latest|:$COMMIT_SHA|g" k8s/*.yaml

# Apply manifests
kubectl apply -f k8s/

# Check rollout status
kubectl rollout status deployment/backend -n fastapi-vue-app
kubectl rollout status deployment/frontend -n fastapi-vue-app
```

---

## Test Coverage

### Backend

| Module | Coverage |
|--------|----------|
| `app/routes` | 73% |
| `app/services` | 55% |
| `app/schemas` | 100% |
| **Total** | **79%** |

### Improving Coverage

1. Add more test cases in `backend/tests/`
2. Test error paths and edge cases
3. Add integration tests with database

---

## Troubleshooting

### Common Pipeline Failures

| Issue | Solution |
|-------|----------|
| Missing secrets | Add required GitHub secrets |
| Docker build fails | Check Dockerfile syntax |
| Test failures | Run tests locally first |
| Deployment timeout | Increase rollout timeout |

### viewing Logs

```bash
# GitHub Actions
# Go to Actions tab > Select workflow run > View logs

# GitLab CI
# Go to CI/CD > Pipelines > Select pipeline > View jobs

# AKS Pods
kubectl logs -f deployment/backend -n fastapi-vue-app
kubectl logs -f deployment/frontend -n fastapi-vue-app
```