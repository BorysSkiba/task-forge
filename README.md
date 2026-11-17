# TaskForge

A secure project and task management REST API built with **FastAPI, PostgreSQL, SQLAlchemy, and Docker**, featuring JWT authentication, user-owned resources, automated testing, rate limiting, and security-focused API design.

![TaskForge Dashboard](docs/images/dashboard.png)

> The desktop interface shown above is an example PySide6 client built to demonstrate how applications can consume the TaskForge REST API.

---

## Overview

TaskForge is a backend-focused project created to explore the design of a production-style REST API beyond basic CRUD functionality.

The API allows users to create and manage projects and tasks while enforcing authentication, ownership, validation, and access-control rules.

The project includes:

- JWT-based user authentication
- secure password hashing with Argon2
- user-owned projects and tasks
- project/task relationships
- filtering, sorting, and pagination
- strict request validation
- rate limiting
- PostgreSQL persistence
- SQLAlchemy ORM
- Alembic database migrations
- automated tests with pytest
- Dockerized application and database
- OWASP-focused API security hardening

---

## Architecture

![TaskForge Architecture](docs/images/architecture.png)

The API is the core of TaskForge.

The included showcase desktop client communicates exclusively through HTTP requests and does not access the database directly.

```text
PySide6 Showcase Client
        │
        │ REST API + JWT
        ▼
FastAPI Application
        │
        ├── Pydantic validation
        ├── JWT authentication
        ├── resource authorization
        ├── rate limiting
        └── trusted host validation
        │
        ▼
SQLAlchemy ORM
        │
        ▼
PostgreSQL
```

FastAPI and PostgreSQL can be launched together using Docker Compose.

---

## Features

### Authentication

Users can register and authenticate using username and password credentials.

Successful login returns a JWT access token used for protected API requests.

Passwords are never stored directly. They are hashed using Argon2 before being persisted.

### Projects

Authenticated users can:

- create projects
- retrieve their projects
- retrieve individual projects
- update projects
- delete projects

A user cannot access projects belonging to another account.

### Tasks

Authenticated users can:

- create tasks
- assign tasks to their own projects
- retrieve tasks
- update tasks
- mark tasks as completed
- remove tasks
- unassign tasks from projects

Task ownership is determined by the authenticated user on the server and cannot be supplied or overridden by the client.

### Filtering and pagination

Task listings support:

- completion filtering
- project filtering
- sorting
- ascending / descending order
- offset pagination
- configurable result limits

Pagination limits are bounded to prevent excessively large queries.

---

## Example Client

A lightweight **PySide6 desktop client** was created as a presentation layer for the API.

It demonstrates:

- JWT login
- project navigation
- task creation
- task editing
- task deletion
- completion state changes
- project-specific task views
- search and status filtering
- live project/task statistics

![Project View](docs/images/project-view.png)

### Task creation

![Create Task](docs/images/create-task.png)

The showcase application is not required to use the API. Any HTTP client capable of sending authenticated REST requests can interact with TaskForge.

---

## API

TaskForge exposes the following routes:

| Method | Endpoint | Authentication | Description |
|---|---|---:|---|
| GET | `/` | No | API health/root endpoint |
| POST | `/users/register` | No | Register a user |
| POST | `/users/login` | No | Authenticate and obtain JWT |
| GET | `/users/me` | Yes | Retrieve current user |
| GET | `/projects` | Yes | Retrieve user's projects |
| POST | `/projects` | Yes | Create project |
| GET | `/projects/{project_id}` | Yes | Retrieve project |
| PATCH | `/projects/{project_id}` | Yes | Update project |
| DELETE | `/projects/{project_id}` | Yes | Delete project |
| GET | `/tasks` | Yes | Retrieve/filter tasks |
| POST | `/tasks` | Yes | Create task |
| GET | `/tasks/{task_id}` | Yes | Retrieve task |
| PATCH | `/tasks/{task_id}` | Yes | Update task |
| DELETE | `/tasks/{task_id}` | Yes | Delete task |

Interactive API documentation is available during development through FastAPI Swagger UI.

![TaskForge API](docs/images/swagger.png)

API documentation can be disabled through application configuration for production-style environments.

---

## Security

Security was treated as part of the API design rather than an afterthought.

### Authentication and passwords

- JWT bearer authentication
- token expiration
- Argon2 password hashing
- generic authentication errors to avoid revealing whether a username exists
- rate limiting on login and registration endpoints

### Object-level authorization

Every project and task belongs to a specific user.

Resource queries validate both:

```text
resource ID
+
authenticated user ID
```

Requests for another user's resources return `404 Not Found` rather than revealing whether the resource exists.

This protects against **Broken Object Level Authorization (BOLA)** attacks.

### Property-level protection

Sensitive ownership properties such as `user_id` are controlled by the server.

Pydantic schemas use explicit allowed fields and reject unexpected properties, preventing clients from injecting ownership or other protected values.

### Input validation

The API validates:

- username length and format
- email addresses
- password length
- task title length
- project name length
- description length
- positive IDs
- pagination bounds
- allowed sorting fields
- allowed sorting directions

Unexpected fields are rejected.

### Rate limiting

Rate limiting protects against brute-force and resource-consumption attacks.

Stricter limits are applied to authentication endpoints, while project and task endpoints share a broader API request limit.

### Host validation

`TrustedHostMiddleware` restricts accepted HTTP host headers and rejects unexpected hosts.

### Dependency security

Python dependencies are checked using:

```bash
pip check
pip-audit
```

Dependencies with known security issues are updated or reviewed before release.

---

## OWASP API Security Review

TaskForge was reviewed against the **OWASP API Security Top 10**.

| Risk | Status |
|---|---|
| Broken Object Level Authorization | Protected and tested |
| Broken Authentication | JWT, hashing, rate limiting |
| Broken Object Property Level Authorization | Strict schemas and server-owned fields |
| Unrestricted Resource Consumption | Pagination and request rate limits |
| Broken Function Level Authorization | Protected authenticated operations |
| Sensitive Business Flows | Not applicable to current functionality |
| Server-Side Request Forgery | Not applicable |
| Security Misconfiguration | Hardened configuration and trusted hosts |
| Improper Inventory Management | Documented endpoint inventory |
| Unsafe Consumption of APIs | Not applicable |

### Function-level authorization

TaskForge currently contains no administrative or role-specific functionality.

Sensitive task and project operations require authentication, while ownership checks ensure users can only operate on their own resources.

---

## Testing

The project contains automated tests for:

- registration
- duplicate users
- login
- invalid credentials
- JWT authentication
- invalid and expired JWT tokens
- task CRUD
- project CRUD
- task authorization between users
- project authorization between users
- cross-user project assignment attempts
- input validation
- pagination validation
- SQL injection-style inputs
- data leakage
- rate limiting
- trusted hosts
- API documentation configuration

Run the test suite with:

```bash
pytest
```

For verbose output:

```bash
pytest -v
```

---

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Alembic
- PyJWT
- pwdlib / Argon2
- SlowAPI

### Testing

- pytest
- FastAPI TestClient
- HTTPX

### Infrastructure

- Docker
- Docker Compose

### Showcase Client

- PySide6
- Qt Style Sheets

---

## Running with Docker

### 1. Clone the repository

```bash
git clone https://github.com/BorysSkiba/task-forge.git
cd TaskForge
```

### 2. Create the environment file

Copy:

```text
.env.example
```

to:

```text
.env
```

and provide your own local values.

Example structure:

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/taskforge
TEST_DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/taskforge_test
SECRET_KEY=replace_with_a_secure_random_secret

POSTGRES_USER=postgres
POSTGRES_PASSWORD=replace_with_a_secure_password
POSTGRES_DB=taskforge
```

Never commit the real `.env` file.

### 3. Build and start the containers

```bash
docker compose up --build
```

Docker Compose starts:

```text
FastAPI
+
PostgreSQL
```

Alembic migrations are applied during API startup.

### 4. Open the API

```text
http://localhost:8000
```

During development, Swagger documentation is available at:

```text
http://localhost:8000/docs
```

---

## Running locally without Docker

Create and activate a virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

Ensure PostgreSQL is running and the environment variables are configured.

Apply database migrations:

```bash
alembic upgrade head
```

Start the API:

```bash
python -m uvicorn app.main:app --reload
```

---

## Project Structure

```text
TaskForge/
│
├── app/
│   ├── routers/
│   │   ├── projects.py
│   │   ├── tasks.py
│   │   └── users.py
│   │
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── rate_limit.py
│   ├── schemas.py
│   └── security.py
│
├── tests/
│   ├── conftest.py
│   ├── helpers.py
│   ├── test_projects.py
│   ├── test_rate_limits.py
│   ├── test_security.py
│   ├── test_tasks.py
│   └── test_users.py
│
├── alembic/
├── compose.yaml
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## What I Learned

TaskForge started as a CRUD API and gradually evolved into a more complete backend system.

The project provided practical experience with:

- designing REST endpoints
- relational database modeling
- SQLAlchemy relationships
- database migrations
- authentication and authorization
- JWT security
- API validation
- automated testing
- Docker-based development environments
- dependency security
- OWASP API security concepts
- separating a client application from the backend through a REST interface

One of the main lessons from the project was that building a reliable API involves significantly more than implementing CRUD operations. Authentication, authorization, validation, testing, infrastructure, and failure handling all become equally important as the project grows.

---

## Status

**Backend: portfolio-ready**

The current version represents the completed backend/API milestone of TaskForge.

Future development may include expanding the desktop client and adding additional project-management functionality.
