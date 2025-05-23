# Kilsar Django REST API

A Django REST API project for task management with environment-specific configurations and containerized deployment.

## Features
- Todo List Management with Priority Ordering
- Task Completion Tracking
- Email Notifications for Task Updates
- Asynchronous Processing with Celery
- Multi-environment Support
- Containerized Deployment

## Tech Stack
- Python 3.10+
- Django 5.2.1
- Django REST Framework
- PostgreSQL 14
- Redis 6
- Celery
- Docker & Docker Compose
- Nginx (Production/Staging) (just shown in docker compose not fleshed out)

## Project Structure
```
kilsar-django/
├── .env.dev                 # Development environment template
├── .env.example             # Example environment template
├── .env.prod                # Production environment template
├── .env.staging             # Staging environment template
├── deploy.sh                # Deployment script
├── docker-compose.base.yml  # Base Docker Compose configuration
├── docker-compose.dev.yml   # Development Docker Compose configuration
├── docker-compose.prod.yml  # Production Docker Compose configuration
├── docker-compose.staging.yml # Staging Docker Compose configuration
├── Dockerfile               # Docker container configuration
├── manage.py                # Django management script
├── README.md                # Documentation
├── requirements.txt         # Python dependencies
│
├── kilsarDjango/           # Main project configuration
│   ├── celery.py           # Celery configuration
│   ├── urls.py             # Main URL routing
│   ├── __pycache__/        # Python bytecode cache
│   └── settings/           # Environment-specific settings
│       ├── base.py         # Base settings shared across environments
│       ├── dev.py          # Development-specific settings
│       ├── staging.py      # Staging-specific settings
│       └── prod.py         # Production-specific settings
│
├── todolist/               # Main application module
│   ├── admin.py            # Django admin configuration
│   ├── apps.py             # Application configuration
│   ├── models.py           # Data models (Todo and TodoItem)
│   ├── permissions.py      # Custom permissions
│   ├── serializers.py      # REST Framework serializers
│   ├── tasks.py            # Celery tasks for async processing
│   ├── tests.py            # Test suite
│   ├── urls.py             # URL routing for Todo API
│   ├── views.py            # API views
│   └── migrations/         # Database migrations
│       └── 0001_initial.py # Initial database migration
```

## Quick Start

### Prerequisites
- Docker
- Docker Compose
- Git

### Installation
1. Clone the repository:
```bash
git clone https://github.com/yoojs/kilsar-django.git
cd kilsar-django
```

2. Set up environment files:
```bash
#Development
cp .env.dev .env
#Staging
cp .env.staging .env
#Production
cp .env.prod .env
```

3. Run the application:
```bash
# Development
./run.sh dev (command: up, down, build (default: up))

# Staging
./run.sh staging (command: up, down, build (default: up))

# Production
./run.sh prod (command: up, down, build (default: up))
```

### Environment Variables
Create appropriate `.env` files with:
```plaintext
POSTGRES_DB=kilsardb
POSTGRES_USER=kilsaruser
POSTGRES_PASSWORD=yourpassword
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=1  # Set to 0 for production
```

## API Endpoints

### Todo Lists
| Method | Endpoint | Description | Required Data |
|--------|----------|-------------|---------------|
| GET    | /api/todo/ | List all todo lists | None
| POST   | /api/todo/ | Create a new todo list | title, description, ownerId
| GET    | /api/todo/{id}/ | Get specific todo list | None
| PUT    | /api/todo/{id}/ | Update a todo list | title, description, ownerId
| DELETE | /api/todo/{id}/ | Delete a todo list | None

### Todo Items
| Method | Endpoint | Description | Required Data |
|--------|----------|-------------|---------------|
| GET    | /api/todo/{todo_list_id}/items/ | List items in todo list | None
| POST   | /api/todo/{todo_list_id}/items/ | Create new item | desc, ownerId, todo_list
| GET   | /api/todo/{todo_list_id}/items/{item_id} | View specific item | None
| PUT    | /api/todo/{todo_list_id}/items/{item_id}/ | Update item fully | desc, todo_list
| PATCH    | /api/todo/{todo_list_id}/items/{item_id}/ | Update partial item | optional: desc, ownerId, todo_list, order, todo_list, is_complete
| DELETE | /api/todo/{todo_list_id}/items/{item_id}/ | Delete item | None

## Development
### Running Dev and testing

```bash
# Development
./run.sh dev
```
Dev will create a superuser for testing
```bash
username: Admin
password: PasswordAdminTodo
```
API tests can be run in localhost:8000/api/todo

All endpoints must be authenticated with basic authentication

Also tests can be run after starting docker: 

#### Running Tests
```bash
# Run tests
docker compose exec web python manage.py test
```


## Deployment Architecture

### Development
- Django development server
- Debug enabled
- Local email backend
- Auto-reload

### Staging/Production
- Gunicorn WSGI server
- Nginx reverse proxy (not fully implemented just wanted to show idea)
- Redis caching
- SMTP email
- Static file serving via Nginx (not fully implemented just wanted to show idea)
## Settings Structure and Cloud Deployment

### Cloud Provider Support
The modular settings structure supports easy deployment to various cloud providers:

#### AWS
- Use `prod.py` with AWS-specific configurations:
  - AWS RDS for PostgreSQL
  - ElastiCache for Redis
  - S3 for static files
  - SES for emails

```python
# Example AWS configuration in prod.py
AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
```

#### Google Cloud Platform
- Adapt `prod.py` for GCP services:
  - Cloud SQL for PostgreSQL
  - Memorystore for Redis
  - Cloud Storage for static files
  - Cloud Tasks for Celery

```python
# Example GCP configuration in prod.py
GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': '/cloudsql/' + os.environ.get('CLOUD_SQL_CONNECTION_NAME'),
    }
}
```

### Environment-Specific Features
- **Development**: Local services, debug tools
- **Staging**: Cloud services, staging data
- **Production**: Cloud services, performance optimizations

### Deployment Flexibility
1. **Environment Variables**
   - All sensitive configurations via environment variables
   - No hardcoded values
   - Easy integration with CI/CD systems

2. **Service Configuration**
   - Database settings adaptable to any provider
   - Caching backend configurable per environment
   - Email backend switchable between providers

3. **Static Files**
   - Development: Local storage
   - Production/Staging: Cloud storage (S3, GCS, etc.)
   - Configurable CDN support

### Scaling Considerations
- **Horizontal Scaling**
  - Stateless application design
  - Session handling via Redis
  - Cache-ready configuration

- **Service Independence**
  - Separate settings for each service
  - Easy to switch between service providers
  - Modular dependency management

## Design Decisions
### API Design
- Flow of API is from Todo List to Todo Item. e.g api/todos/{todo_list_id}/items/{todo_item_id}
- Could potentially get long, but for a short API relation like todo lists and items I found it to be alright and straight forward.
- Trade-off: Shows strong relational so user can track back and forward vs potentionally long url's and redundant endpoints
### Project Structure
- Main Project as kilsarDjango 
- App project as todolist
- Added all logic of todo list and todo item to one App
- Trade-off: Development ease (can view and check on models and views easier for small api) vs future proofing, could get verbose would split app later if logic becomes large
- 
### Multi-Environment Settings
- Modular settings structure
- Environment-specific configurations
- Configuration via environment variables
- Trade-off: Setup complexity vs deployment flexibility

### Database Choice
- PostgreSQL for reliability and features
- Trade-off: Resource usage vs simplicity

### Asynchronous Processing
- Celery with Redis broker
- Email notifications handling
- Trade-off: Infrastructure complexity vs scalability

### Security Considerations
- Currently using basic authentication with Django
- Would like to use Auth0 and JWT tokens for auth, but felt that may be overkill for small api, but for some authentication service would be good for future proofing, extra security, and user management 
- Trade-off: Django auth is easy to implement and have full control of users vs Auth0 is potentially better security wise (MFA if needed), ease of managing users, and more ways for users to login (Magic links, passwordless etc)

## Limitations and Future Improvements

### Current Limitations
- Basic authentication (Would like to use something like Auth0 for user management and JWT tokens for authentication instead of basic Django authentication)
- Limited test coverage
- Basic error handling

### Planned Improvements
- JWT authentication (auth0)
- Comprehensive testing
- CI/CD pipeline
- Enhanced logging
- API documentation
- Caching layer
- Rate limiting

