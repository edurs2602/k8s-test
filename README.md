# FastAPI + Vue.js - AKS Deployment Project

A full-stack web application designed for deployment on Azure Kubernetes Service (AKS), featuring a FastAPI backend with async PostgreSQL support and a Vue.js frontend.

## 🏗️ Architecture

- **Backend**: FastAPI (Python 3.11+) with async SQLAlchemy ORM
- **Frontend**: Vue.js3 with TypeScript and Pinia state management
- **Database**: Neon PostgreSQL (serverless)
- **Package Manager**: UV (Python), npm (Node.js)
- **Deployment**: Docker containers on AKS

## 📁 Project Structure

```
k8s-test/
├── backend/              # FastAPI application
│   ├── app/              # Application code
│   ├── tests/            # Test suite
│   ├── alembic/          # Database migrations
│   └── Dockerfile
├── frontend/             # Vue.js application
│   ├── src/              # Source code
│   ├── Dockerfile
│   └── nginx.conf
├── k8s/                  # Kubernetes manifests
├── agents/               # AI agent documentation
├── docker-compose.yaml   # Production compose
├── docker-compose.dev.yaml # Development compose
└── Documentation files
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- UV package manager
- Docker and Docker Compose
- Neon PostgreSQL account (free tier available)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd k8s-test
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Neon DATABASE_URL
   ```

3. **Start development environment**
   ```bash
   docker-compose -f docker-compose.dev.yaml up -d
   ```

4. **Access the applications**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Setup (without Docker)

#### Backend Setup

```bash
cd backend

# Install UV if not already installed
pip install uv

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Run database migrations
alembic upgrade head

# Start the development server
uvicorn app.main:app --reload
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🗄️ Database Configuration

### Neon PostgreSQL Setup

1. Create a free account at [Neon](https://neon.tech)
2. Create a new project
3. Copy the connection string
4. Add to your `.env` file:

```bash
DATABASE_URL=postgresql+asyncpg://username:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
```

### Running Migrations

```bash
cd backend
alembic revision -m "description of changes"  # Create migration
alembic upgrade head                            # Apply migrations
alembic downgrade -1                            # Rollback one migration
```

## 🔧 Development

### Backend Commands

```bash
# Run development server
uvicorn app.main:app --reload

# Run tests
pytest

# Format and lint code
ruff format .
ruff check .

# Type check
mypy app
```

### Frontend Commands

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint

# Format code
npm run format
```

## 🐳 Docker

### Build Images

```bash
# Backend
docker build -t your-registry/backend:latest ./backend

# Frontend
docker build -t your-registry/frontend:latest ./frontend
```

### Run with Docker Compose

```bash
# Development
docker-compose -f docker-compose.dev.yaml up -d

# Production
docker-compose up -d
```

## ☸️ Kubernetes Deployment (AKS)

### Prerequisites

- Azure CLI installed
- kubectl configured
- AKS cluster running
- Azure Container Registry (ACR)

### Deployment Steps

1. **Push images to ACR**
   ```bash
   az acr login --name your-registry
   docker tag your-registry/backend:latest your-registry.azurecr.io/backend:latest
   docker push your-registry.azurecr.io/backend:latest
   docker tag your-registry/frontend:latest your-registry.azurecr.io/frontend:latest
   docker push your-registry.azurecr.io/frontend:latest
   ```

2. **Update Kubernetes manifests**
   - Edit `k8s/backend-deployment.yaml` and `k8s/frontend-deployment.yaml`
   - Replace `your-registry.azurecr.io` with your ACR name

3. **Create secrets and config**
   ```bash
   kubectl apply -f k8s/namespace.yaml
   kubectl apply -f k8s/configmap.yaml
   ```

4. **Deploy applications**
   ```bash
   kubectl apply -f k8s/backend-deployment.yaml
   kubectl apply -f k8s/frontend-deployment.yaml
   kubectl apply -f k8s/ingress.yaml
   ```

5. **Verify deployment**
   ```bash
   kubectl get pods -n fastapi-vue-app
   kubectl get services -n fastapi-vue-app
   kubectl get ingress -n fastapi-vue-app
   ```

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| GET | / | API information |
| POST | /items | Create item |
| GET | /items | List items (paginated) |
| GET | /items/{id} | Get item by ID |
| PATCH | /items/{id} | Update item |
| DELETE | /items/{id} | Delete item |

Full API documentation available at `/docs` (Swagger UI) or `/redoc` (ReDoc).

## 📝 Environment Variables

### Backend

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | Neon PostgreSQL connection string | Yes |
| ENVIRONMENT | Environment (development/production) | No |
| DEBUG | Enable debug mode | No |
| CORS_ORIGINS | Allowed CORS origins (JSON array) | No |

### Frontend

| Variable | Description | Required |
|----------|-------------|----------|
| VITE_API_URL | Backend API URL | No (defaults to /api) |

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## 📚 Documentation

- **SKILLS.md** - Technology skills and competencies
- **PLAN.md** - Architecture and implementation plan
- **SOUL.md** - Project philosophy and principles
- **AGENS.md** - AI assistant guidelines

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Vue.js](https://vuejs.org/) - Progressive JavaScript framework
- [Neon](https://neon.tech/) - Serverless PostgreSQL
- [UV](https://github.com/astral-sh/uv) - Fast Python package manager