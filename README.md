# Blog API

A modern, scalable blog API built with Django-Ninja and PostgreSQL.

## Features

- RESTful API for blog post management
- Admin interface for managing blog posts
- PostgreSQL database for data persistence
- Docker support for easy deployment
- Comprehensive logging system
- Secure configuration with environment variables
- API documentation with OpenAPI/Swagger
- Automated testing suite
- Robust request validation using Pydantic schemas
- Continuous Integration/Deployment with GitHub Actions
- Automated testing on every push and pull request
- Comprehensive error handling and validation responses

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- PostgreSQL 17
- Poetry 1.8.2 (Python package manager)

## Project Setup

### Development Setup

1. Clone the repository:

```bash
git clone https://github.com/no13bus/blog
cd blog
```

2. Copy the environment file and configure it:

```bash
cp .env.example .env.dev
```

Edit `.env.dev` with your configuration:

```
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=blog
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=db
DB_PORT=5432
```

3. Start the development server with Poetry:

```bash

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 - --version 1.8.2

# Install dependencies
poetry install

# Activate Poetry shell
poetry shell

# Apply database migrations
./manage.py migrate
# Create a superuser for admin access
./manage.py createsuperuser
# run the server
./manage.py runserver 0.0.0.0:8000
```

### Production Setup

1. Copy the production environment file:

```bash
cp .env.example .env.prod
```

2. Configure production settings in `.env.prod`

3. Build and run the production containers:

```bash
docker-compose build
docker-compose up -d
# Apply database migrations
docker-compose exec web python manage.py migrate
# Create a superuser for admin access
docker-compose exec web python manage.py createsuperuser
```

## API Documentation and Usage

### Interactive Documentation

The API documentation is available through Swagger UI at:

- `http://localhost:8000/api/docs`

### Admin Interface

`http://localhost:8000/admin/`

### API Endpoints

#### Posts

1. List all posts

```bash
GET /api/v1/posts

# Example response
{
    "posts": [
        {
            "id": 1,
            "title": "First Blog Post",
            "content": "This is the content of my first blog post",
            "created_at": "2025-03-20T10:00:00Z",
            "updated_at": "2025-03-20T10:00:00Z"
        }
    ]
}
```

2. Create a new post

```bash
POST /api/v1/posts
Content-Type: application/json

{
    "title": "My New Post",
    "content": "This is the content of my new blog post"
}

# Example response
{
    "id": 2,
    "title": "My New Post",
    "content": "This is the content of my new blog post",
    "created_at": "2025-03-20T11:00:00Z",
    "updated_at": "2025-03-20T11:00:00Z"
}
```

3. Get a specific post

```bash
GET /api/v1/posts/{post_id}

# Example response
{
    "id": 1,
    "title": "First Blog Post",
    "content": "This is the content of my first blog post",
    "created_at": "2025-03-20T10:00:00Z",
    "updated_at": "2025-03-20T10:00:00Z"
}
```

4. Update a post

```bash
PUT /api/v1/posts/{post_id}
Content-Type: application/json

{
    "title": "Updated Title",
    "content": "Updated content for my blog post"
}

# Example response
{
    "id": 1,
    "title": "Updated Title",
    "content": "Updated content for my blog post",
    "created_at": "2025-03-20T10:00:00Z",
    "updated_at": "2025-03-20T12:00:00Z"
}
```

5. Delete a post

```bash
DELETE /api/v1/posts/{post_id}

# Example response
{
    "message": "Post deleted successfully"
}
```

### Authentication

The API supports token-based authentication. To enable authentication, uncomment this line in `blog/urls.py`:

```python
api.add_router("/v1", post_api_v1, auth=APIAuthBearer())
```

#### Getting a Token

```bash
# Create a token for a user
POST /api/v1/auth/token
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}

# Response
{
    "token": "your_access_token"
}
```

Token features:

- Secure random token generation
- 24-hour expiration
- Automatic validation on protected endpoints
- Invalid credentials return 401 error

#### Using Authentication

Add the token to your request headers:

```bash
# Example of authenticated request
curl http://localhost:8000/api/v1/posts \
  -H "Authorization: Bearer your_access_token"

# Create a post with authentication
curl -X POST http://localhost:8000/api/v1/posts \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Post", "content": "Post content"}'
```

### Using cURL

Here are some example cURL commands to interact with the API:

```bash
# List all posts
curl http://localhost:8000/api/v1/posts

# Create a new post
curl -X POST http://localhost:8000/api/v1/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "My New Post", "content": "Post content here"}'

# Get a specific post
curl http://localhost:8000/api/v1/posts/1

# Update a post
curl -X PUT http://localhost:8000/api/v1/posts/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "content": "Updated content"}'

# Delete a post
curl -X DELETE http://localhost:8000/api/v1/posts/1
```

### Error Responses

The API returns appropriate HTTP status codes and error messages:

```json
{
  "error": "Error message here"
}
```

Common status codes:

- 200: Successful operation
- 201: Resource created
- 422: validation error
- 404: Resource not found
- 500: Server error

## Design Decisions

1. **Architecture**

   - Service layer pattern to encapsulate business logic:
     - Clear separation of concerns
     - Reusable business logic
     - Easier testing and maintenance
   - Django Ninja for modern API development:
     - Fast performance with async support
     - Type hints and automatic validation via Pydantic
     - Auto-generated OpenAPI/Swagger documentation
     - Lightweight alternative to DRF
   - Environment configuration using .env files for dev/prod settings

2. **Request Validation**

   - Implemented comprehensive request validation using Pydantic schemas
   - Strict field validation with clear error messages
   - Title field: Required, 1-200 characters
   - Content field: Required, 1-1000 characters
   - Standardized error response format for validation failures

3. **Automated Testing & CI/CD**

   - GitHub Actions workflow for automated testing
   - Tests run on every push and pull request

4. **Error Logging**

   - Centralized error logging system
   - JSON-formatted logs for better parsing
   - Separate log files for different concerns:
     - API logs: `/logs/api.log`
     - Application logs: `/logs/django.log`
   - Log rotation to manage file sizes

5. **Database**

   - PostgreSQL for robust JSON support
   - Optimized indexing on title field

6. **Dependency Management**

   - Poetry for reliable and reproducible builds:
     - Deterministic dependency resolution
     - Lock file ensures consistent installations
     - Isolated virtual environments
     - Easy package version management

7. **Containerization**
   - Optimized Docker build with layer caching strategy:
     - Separate dependency installation layer for faster rebuilds
     - Slim base image for reduced container size
   - Production-ready Docker configuration:
     - Nginx for reverse proxy and static file serving
     - Gunicorn as WSGI application server
     - PostgreSQL in separate container
