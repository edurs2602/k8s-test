# AGENS.md

## AI Assistant Guidelines for This Project

This document provides guidelines for AI assistants (like Claude, GPT-4, etc.) working on this codebase.

---

## Project Context

### What This Project Is
A full-stack web application with:
- **Backend**: FastAPI (Python 3.11+) with async SQLAlchemy
- **Frontend**: Vue.js 3 with TypeScript and Pinia
- **Database**: Neon PostgreSQL (serverless)
- **Deployment**: Azure Kubernetes Service (AKS)

### What This Project Is NOT
- A production-ready enterprise application
- A tutorial or demo project
- A monolithic architecture

---

## Code Style Guidelines

### Python (Backend)

#### Naming Conventions
```python
# Classes: PascalCase
class ItemService:
    pass

# Functions/Variables: snake_case
async def get_items():
    item_list = []

# Constants: UPPER_SNAKE_CASE
MAX_ITEMS_PER_PAGE = 100

# Private methods: leading underscore
def _internal_helper():
    pass
```

#### Type Hints
```python
# Always use type hints
async def get_by_id(db: AsyncSession, item_id: int) -> Item | None:
    pass

# Use Pydantic models for schemas
class ItemCreate(BaseModel):
    title: str
    description: str | None = None
```

#### Async Patterns
```python
# Use async/await for all I/O
async def create_item(db: AsyncSession, item: ItemCreate) -> Item:
    db_item = Item(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item
```

### TypeScript (Frontend)

#### Naming Conventions
```typescript
// Interfaces: PascalCase
interface Item {
  id: number
  title: string
}

// Variables: camelCase
const itemList = ref<Item[]>([])

// Functions: camelCase
async function fetchItems() {}

// Constants: UPPER_SNAKE_CASE or camelCase for React/Vue
const API_BASE_URL = '/api'
```

#### Vue Composition API
```vue
<script setup lang="ts">
// Use <script setup> syntax
import { ref, onMounted } from 'vue'

// Reactive state
const items = ref<Item[]>([])

// Methods
async function fetchData() {
  // ...
}

// Lifecycle
onMounted(() => {
  fetchData()
})
</script>
```

### Kubernetes Manifests

#### Naming Conventions
- Resources: kebab-case (e.g., `backend-deployment`)
- Labels: app/name pattern
- Namespaces: kebab-case

#### Structure
```yaml
# Always include:
# - Resource limits
# - Health checks
# - Labels
# - Namespace

apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: fastapi-vue-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    # ... pod spec
```

---

## File Organization

### When Adding New Features

#### Backend
1. Create model in `backend/app/models/`
2. Create schema in `backend/app/schemas/`
3. Create service in `backend/app/services/`
4. Create routes in `backend/app/routes/`
5. Register router in `backend/app/main.py`
6. Create Alembic migration: `alembic revision -m "add_new_table"`

#### Frontend
1. Create types in `frontend/src/types/`
2. Create API methods in `frontend/src/api/`
3. Create store in `frontend/src/stores/`
4. Create components in `frontend/src/components/`
5. Create views in `frontend/src/views/`
6. Add route in `frontend/src/router/index.ts`

---

## Common Tasks

### Adding a New API Endpoint

1. **Model** (`backend/app/models/example.py`):
```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel

class Example(BaseModel):
    __tablename__ = "examples"
    name: Mapped[str] = mapped_column(String(255), nullable=False)
```

2. **Schema** (`backend/app/schemas/example.py`):
```python
from pydantic import BaseModel

class ExampleCreate(BaseModel):
    name: str

class ExampleResponse(ExampleCreate):
    id: int
```

3. **Service** (`backend/app/services/example_service.py`):
```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.example import Example
from app.schemas.example import ExampleCreate

class ExampleService:
    @staticmethod
    async def create(db: AsyncSession, data: ExampleCreate) -> Example:
        example = Example(**data.model_dump())
        db.add(example)
        await db.commit()
        return example
```

4. **Route** (`backend/app/routes/examples.py`):
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services import ExampleService

router = APIRouter(prefix="/examples", tags=["examples"])

@router.post("/", status_code=201)
async def create_example(
    data: ExampleCreate,
    db: AsyncSession = Depends(get_db)
):
    return await ExampleService.create(db, data)
```

### Adding a New Vue Component

```vue
<!-- frontend/src/components/ExampleCard.vue -->
<script setup lang="ts">
import type { Example } from '@/types/example'

defineProps<{
  example: Example
}>()
</script>

<template>
  <div class="example-card">
    <h3>{{ example.name }}</h3>
  </div>
</template>

<style scoped>
.example-card {
  padding: 1rem;
  border: 1px solid #ddd;
}
</style>
```

---

## Testing Guidelines

### Backend Tests
```python
# backend/tests/test_items.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_item(client: AsyncClient):
    response = await client.post("/api/items", json={
        "title": "Test Item",
        "description": "Test description"
    })
    assert response.status_code == 201
```

### Frontend Tests
```typescript
// frontend/src/components/__tests__/ItemList.test.ts
import { mount } from '@vue/test-utils'
import ItemList from '@/components/ItemList.vue'

describe('ItemList', () => {
  it('renders items correctly', () => {
    const wrapper = mount(ItemList, {
      props: { items: [] }
    })
    expect(wrapper.find('.empty').exists()).toBe(true)
  })
})
```

---

## Environment Variables

### Backend Variables
```bash
DATABASE_URL=postgresql+asyncpg://...
ENVIRONMENT=production|development
DEBUG=true|false
CORS_ORIGINS=["https://example.com"]
```

### Frontend Variables
```bash
VITE_API_URL=/api  # or full URL for production
```

---

## Deployment Checklist

- [ ] Update environment variables
- [ ] Run database migrations
- [ ] Build Docker images
- [ ] Push images to registry
- [ ] Apply Kubernetes manifests
- [ ] Verify health checks
- [ ] Check ingress routing
- [ ] Test SSL/TLS (if applicable)

---

## Troubleshooting

### Common Issues

#### Database Connection Errors
- Check DATABASE_URL format
- Verify SSL mode (Neon requires SSL)
- Ensure connection string includes `?ssl=require`

#### CORS Errors
- Add frontend URL to CORS_ORIGINS
- Check preflight request handling
- Verify proxy configuration in vite.config.ts

#### Kubernetes Pods Not Starting
- Check resource limits
- Verify image exists in registry
- Check environment variables
- Review pod logs: `kubectl logs <pod-name>`

---

## AI Assistant Best Practices

When assisting with this project:

1. **Preserve Structure**: Follow existing patterns
2. **Add Types**: Always include type hints/annotations
3. **Document**: Add docstrings for complex logic
4. **Test**: Suggest tests for new features
5. **Security**: Highlight security concerns
6. **Performance**: Consider async and efficiency
7. **Compatibility**: Maintain Python 3.11+ and Node20+
8. **Keep It Simple**: Avoid over-engineering

---

## Need Help?

Check these resources:
- FastAPI Docs: https://fastapi.tiangolo.com/
- Vue 3 Docs: https://vuejs.org/
- SQLAlchemy 2.0: https://docs.sqlalchemy.org/
- Neon Docs: https://neon.tech/docs/
- AKS Docs: https://docs.microsoft.com/azure/aks/