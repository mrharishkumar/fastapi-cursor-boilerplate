# FastAPI Cursor Boilerplate

A modern, production-ready FastAPI boilerplate with best practices, code quality tools, and Docker support.

## Features

- ⚡ **FastAPI** - High-performance async Python web framework
- 🗄️ **SQLAlchemy + pyodbc** - Database ORM with SQL Server support
- 🔧 **UV** - Ultra-fast Python package manager and project management
- 🎯 **Ruff** - Lightning-fast Python linter and formatter
- 🐳 **Docker** - Containerized development and production environments
- 🛠️ **Make** - Simple command runner with helpful shortcuts
- 📦 **Pre-commit hooks** - Automated code quality checks
- 🎯 **Cursor Rules** - Comprehensive coding standards and architectural guidelines
- 🔍 **Type hints** - Full type annotation support
- 📚 **Interactive API docs** - Swagger UI and ReDoc documentation
- 🏥 **Health checks** - Database and application monitoring endpoints
- 📝 **Structured logging** - Loguru-based logging with file rotation

## Cursor Rules

This boilerplate includes comprehensive Cursor rules that enforce:

- **Architectural Standards**: Layered architecture with clear separation of concerns
- **API Design Patterns**: RESTful conventions, Pydantic validation, and proper router structure
- **Testing & Security**: High test coverage, environment variable management, and security best practices
- **Code Organization**: Consistent project structure, naming conventions, and modular design

The rules automatically apply to all Python files and help maintain code quality and consistency.

## Prerequisites

- **SQL Server**: Local installation of Microsoft SQL Server (2019 or later)
- **Docker**: For containerized development (recommended)
- **UV**: Python package manager (for local development)

## Quick Start

### Option 1: Docker with Local SQL Server (Recommended)

This setup runs the FastAPI application in Docker while connecting to your locally installed SQL Server.

1. **Ensure SQL Server is running locally** and accessible on `localhost`

2. **Configure environment:**
```bash
cp env.example .env
# Edit .env with your local SQL Server configuration
```

3. **Start the application:**
```bash
# Development
make docker-up

# Production
make docker-prod-up
```

The Docker container will connect to your local SQL Server using `host.docker.internal` to access the host machine.

### Option 2: Local Development

1. **Install dependencies:**
```bash
uv sync
uv pip install .[dev]
```

2. **Configure environment:**
```bash
cp env.example .env
# Edit .env with your database configuration
```

3. **Run the application:**
```bash
make dev
```

The API will be available at `http://localhost:8000`

## Available Commands

Run `make help` to see all available commands:

```bash
make help
```

## API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## Health Checks

- **Basic health**: `http://localhost:8000/api/v1/health`
- **Database health**: `http://localhost:8000/api/v1/health/database`

## Database Configuration

The application uses SQLAlchemy with pyodbc for SQL Server. For Docker development, the container connects to your local SQL Server installation.

### Local SQL Server Setup

1. **Install SQL Server** (2019 or later) on your local machine
2. **Enable TCP/IP** connections in SQL Server Configuration Manager
3. **Create a database** for the application (e.g., `fastapi_db`)
4. **Configure SQL Server Authentication** or use Windows Authentication

### Environment Configuration

Configure via environment variables in your `.env` file:

```env
# For Docker development (connects to local SQL Server)
DATABASE_DRIVER=ODBC Driver 18 for SQL Server
DATABASE_SERVER=host.docker.internal  # For Docker containers
# DATABASE_SERVER=localhost  # For local development

DATABASE_NAME=fastapi_db
DATABASE_USERNAME=sa
DATABASE_PASSWORD=your_secure_password_here
DATABASE_TRUSTED_CONNECTION=false
```

**Note**: When using Docker, the container uses `host.docker.internal` to access your local SQL Server. For local development, use `localhost` instead.

## Environment Variables

| Variable | Description | Default | Docker Note |
|----------|-------------|---------|-------------|
| `DATABASE_DRIVER` | ODBC driver name | `ODBC Driver 18 for SQL Server` | - |
| `DATABASE_SERVER` | Database server | `localhost` | Use `host.docker.internal` for Docker |
| `DATABASE_NAME` | Database name | `fastapi_db` | - |
| `DATABASE_USERNAME` | Database username | `sa` | - |
| `DATABASE_PASSWORD` | Database password | `your_secure_password_here` | - |
| `DATABASE_TRUSTED_CONNECTION` | Windows auth | `false` | - |
| `LOG_LEVEL` | Logging level | `INFO` | - |

## Logging

Uses Loguru for structured logging:
- **`logs/app.log`** - Application logs with rotation
- **`logs/error.log`** - Error logs only

```python
from app.core.logging import get_logger
logger = get_logger(__name__)
logger.info("Application started")
```

## Production Deployment

```bash
# Run with Docker
make docker-prod-up
```
