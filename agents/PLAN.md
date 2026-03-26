# PLAN.md

## Project Architecture & Implementation Plan

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client (Browser)                        │
└─────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Vue.js Frontend (SPA)                         │
│  - Vue 3 + Composition API                                      │
│  - Pinia State Management                                        │
│  - Vue Router                                                    │
│  - Axios HTTP Client                                             │
│  - TailwindCSS Styling                                           │
└─────────────────────────────────────────────────────────────────┘
                                   │
                                   │ HTTP/REST API
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                               │
│  - REST API Endpoints                                            │
│  - Pydantic Validation                                           │
│  - Async SQLAlchemy ORM                                          │
│  - CORS Middleware                                                │
└─────────────────────────────────────────────────────────────────┘
                                   │
                                   │ Async PostgreSQL Connection
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Neon PostgreSQL                               │
│  - Serverless PostgreSQL                                         │
│  - Auto-scaling                                                  │
│  - Connection Pooling                                            │
└─────────────────────────────────────────────────────────────────┘
```

### Project Structure

```
k8s-test/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI application entry
│   │   ├── config.py                 # Pydantic settings
│   │   ├── database.py               # SQLAlchemy async setup
│   │   ├── models/                   # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # Base model with timestamps
│   │   │   └── item.py               # Example Item model
│   │   ├── schemas/                  # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   └── item.py               # Item request/response schemas
│   │   ├── routes/                   # API route handlers
│   │   │   ├── __init__.py
│   │   │   └── items.py              # Item CRUD endpoints
│   │   └── services/                 # Business logic layer
│   │       ├── __init__.py
│   │       └── item_service.py       # Item service functions
│   ├── tests/                        # Test suite
│   ├── alembic/                      # Database migrations
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── alembic.ini
│   ├── pyproject.toml                # UV project configuration
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                         # Vue.js Frontend
│   ├── src/
│   │   ├── main.ts                   # App entry point
│   │   ├── App.vue                   # Root component
│   │   ├── style.css                 # Global styles + Tailwind
│   │   ├── router/                   # Vue Router configuration
│   │   │   └── index.ts
│   │   ├── stores/                   # Pinia stores
│   │   │   └── items.ts              # Items state management
│   │   ├── components/               # Reusable components
│   │   │   └── ItemList.vue
│   │   ├── views/                    # Page components
│   │   │   └── Home.vue
│   │   ├── types/                    # TypeScript interfaces
│   │   │   └── item.ts
│   │   └── api/                      # API client
│   │       └── index.ts
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── Dockerfile
│   ├── nginx.conf                    # Nginx configuration
│   └── .env.example
│
├── k8s/                              # Kubernetes manifests
│   ├── namespace.yaml                # Namespace + Secrets
│   ├── configmap.yaml                # App configuration
│   ├── backend-deployment.yaml       # Backend deployment + service
│   ├── frontend-deployment.yaml      # Frontend deployment + service
│   └── ingress.yaml                  # Ingress routing
│
├── agents/                           # AI agent documentation
├── docker-compose.yaml               # Production compose
├── docker-compose.dev.yaml           # Development compose
├── .env.example
├── SKILLS.md                         # Technology skills
├── PLAN.md                           # Architecture plan
├── SOUL.md                           # Project philosophy
├── AGENS.md                          # Agent guidelines
└── README.md                         # Project documentation
```

### Implementation Phases

#### Phase 1: Project Setup ✅
- [x] Initialize project structure
- [x] Configure UV for Python package management
- [x] Setup FastAPI with async SQLAlchemy
- [x] Configure Vue 3 with Vite and TypeScript
- [x] Setup TailwindCSS for styling

#### Phase 2: Backend Development ✅
- [x] Create database models with SQLAlchemy
- [x] Implement CRUD operations (Create, Read, Update, Delete)
- [x] Setup Pydantic schemas for validation
- [x] Configure CORS for frontend communication
- [x] Add health check endpoints

#### Phase 3: Frontend Development ✅
- [x] Create Vue components with Composition API
- [x] Implement state management with Pinia
- [x] Setup Vue Router for navigation
- [x] Create API client with Axios
- [x] Implement TypeScript interfaces

#### Phase 4: Infrastructure ✅
- [x] Create Dockerfiles for backend and frontend
- [x] Configure docker-compose for local development
- [x] Create Kubernetes manifests for AKS
- [x] Setup ingress configuration
- [x] Configure secrets and configmaps

#### Phase 5: Testing & Deployment (TODO)
- [ ] Add unit tests for backend
- [ ] Add component tests for frontend
- [ ] Setup CI/CD pipeline
- [ ] Deploy to AKS
- [ ] Configure SSL/TLS with cert-manager

### Database Schema

#### Items Table
```sql
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### API Endpoints

| Method |Endpoint | Description |
|--------|---------|-------------|
| GET | /health | Health check endpoint |
| GET | / | API information |
| POST | /items | Create new item |
| GET | /items | List all items (paginated) |
| GET | /items/{id} | Get item by ID |
| PATCH | /items/{id} | Update item |
| DELETE | /items/{id} | Delete item |

### Deployment Strategy

#### Local Development
```bash
# Start development environment
docker-compose -f docker-compose.dev.yaml up -d

# Backend runs on http://localhost:8000
# Frontend runs on http://localhost:5173
# API docs available at http://localhost:8000/docs
```

#### Production Deployment (AKS)
1. Build and push Docker images to Azure Container Registry
2. Apply Kubernetes manifests
3. Configure ingress with SSL
4. Setup monitoring with Azure Monitor

### Security Considerations
- Environment variables for secrets
- CORS configuration for allowed origins
- SSL/TLS encryption in transit
- Non-root container users
- Resource limits in Kubernetes
- Secrets management in Kubernetes