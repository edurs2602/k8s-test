# SOUL.md

## Project Philosophy & Principles

### Core Values

#### 1. Simplicity First
We believe in keeping things simple and focused. Every component should have a single responsibility and be easy to understand, test, and maintain. We avoid over-engineering and unnecessary complexity.

#### 2. Modern Best Practices
This project embraces modern development practices:
- **Async/Await**: Full async support for better performance
- **Type Safety**: TypeScript on frontend, type hints on backend
- **Composition Over Inheritance**: Vue Composition API, functional services
- **Separation of Concerns**: Clear boundaries between layers

#### 3. Developer Experience
We prioritize developer experience with:
- Fast feedback loops (Vite HMR, uvicorn --reload)
- Clear project structure
- Comprehensive documentation
- Easy local development setup

---

## Design Decisions

### Why FastAPI?
- **Performance**: Async support makes it one of the fastest Python frameworks
- **Developer Productivity**: Automatic OpenAPI docs save time
- **Type Safety**: Pydantic integration catches errors early
- **Modern**: Built for Python 3.11+ with type hints

### Why Vue.js 3?
- **Approachable**: Easy to learn, progressive framework
- **Performance**: Optimized reactivity system
- **TypeScript Support**: First-class TypeScript integration
- **Composition API**: Better code organization and reusability

### Why Neon PostgreSQL?
- **Serverless**: No server management required
- **Auto-scaling**: Handles traffic spikes automatically
- **Developer Friendly**: Free tier for development
- **Modern**: Built for cloud-native applications

### Why Kubernetes (AKS)?
- **Scalability**: Easy horizontal scaling
- **Resilience**: Self-healing capabilities
- **Cloud Native**: Standard for modern deployments
- **Learning**: Industry-standard skill set

---

## Code Philosophy

### Python Backend
```python
# We prefer explicit over implicit
from app.services import ItemService
item = await ItemService.get_by_id(db, item_id)

# Clear naming and structure
class ItemService:
    @staticmethod
    async def create(db: AsyncSession, item_data: ItemCreate) -> Item:
        # One responsibility: create an item
        pass
```

### TypeScript Frontend
```typescript
// Strong typing for safety
interface Item {
  id: number
  title: string
  description: string | null
  is_active: boolean
}

// Composition API for clarity
const itemStore = useItemStore()
await itemStore.fetchItems()
```

### Infrastructure as Code
```yaml
# Declarative configuration
# Everything versioned in Git
# Reproducible deployments
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
```

---

## Quality Standards

### Code Quality
- **Linting**: Ruff for Python, ESLint for TypeScript
- **Type Checking**: MyPy for Python, TypeScript for frontend
- **Formatting**: Consistent code style across the project

### Testing Philosophy
- **Unit Tests**: Test individual functions/components
- **Integration Tests**: Test API endpoints end-to-end
- **E2E Tests**: Test user flows in the browser

### Documentation Standards
- **Code Comments**: Explain "why", not "what"
- **README**: Quick start guide
- **Architecture Docs**: System design decisions
- **API Docs**: Auto-generated from OpenAPI spec

---

## Performance Principles

### Backend
1. **Async Everything**: Use async/await for I/O operations
2. **Connection Pooling**: Reuse database connections
3. **Efficient Queries**: Only fetch what you need
4. **Caching**: Consider Redis for frequently accessed data

### Frontend
1. **Code Splitting**: Lazy load routes and components
2. **Bundle Size**: Keep dependencies minimal
3. **Optimistic Updates**: Update UI before API response
4. **Responsive Design**: Mobile-first approach

### Infrastructure
1. **Resource Limits**: Set appropriate limits in Kubernetes
2. **Health Checks**: Ready and liveness probes
3. **Monitoring**: Application metrics and logs
4. **CDN**: Serve static assets from CDN (future)

---

## Security Mindset

### Authentication & Authorization
- Currently: No authentication (as per requirements)
- Future ready: Easy to add JWT/OAuth2

### Data Protection
- Environment variables for secrets
- SSL/TLS for all connections
- Input validation with Pydantic
- Parameterized queries (SQLAlchemy)

### Infrastructure Security
- Non-root containers
- Network policies (future)
- Regular security updates
- Secrets management in Kubernetes

---

## Team Values

### Communication
- **Clear Documentation**: Self-documenting code + README
- **Commit Messages**: Meaningful, descriptive messages
- **Code Reviews**: Constructive feedback, not criticism

### Learning
- **Modern Stack**: Stay current with best practices
- **Experimentation**: Try new approaches in sandbox
- **Knowledge Sharing**: Document learnings

### Collaboration
- **Open Source**: MIT license for flexibility
- **Conventional Commits**: Standardized commit messages
- **Pull Request Template**: Consistent PR format