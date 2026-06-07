# Course Enrollment Platform API

A secure, database-backed RESTful API for managing a course enrollment platform. Built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy (async)**, featuring JWT authentication, role-based access control, and a full automated test suite. Fully containerized with Docker.


## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Local Setup](#local-setup)
- [Running Migrations](#running-migrations)
- [Running the Server](#running-the-server)
- [Docker Deployment](#docker-deployment)
- [Running Tests](#running-tests)
- [API Overview](#api-overview)
- [Role-Based Access Control](#role-based-access-control)
- [Environment Variables](#environment-variables)


## Features

- JWT-based authentication (register, login, protected routes)
- Role-based access control (Student vs Admin)
- Full course management (create, update, activate/deactivate, delete)
- Enrollment management with business rule enforcement:
  - Prevents duplicate enrollments
  - Enforces course capacity limits
  - Blocks enrollment in inactive courses
- Admin oversight (view all enrollments, remove students from courses)
- Async database access with SQLAlchemy
- Database migrations with Alembic (auto-runs on Docker startup)
- Automated test suite with pytest and in-memory SQLite


## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy (async) |
| Migrations | Alembic |
| Authentication | JWT via python-jose |
| Password Hashing | passlib + bcrypt |
| Validation | Pydantic v2 |
| Containerization | Docker + Docker Compose |
| Testing | pytest, pytest-asyncio, httpx |
| Test Database | SQLite in-memory via aiosqlite |



## Project Structure


Course_Enrollment_Platform_API/
├── alembic/                        # Migration files
│   └── versions/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py             # Auth endpoints (register, login, me)
│   │       ├── user.py             # User endpoints
│   │       ├── course.py           # Course endpoints
│   │       └── enrollment.py       # Enrollment endpoints
│   ├── core/
│   │   ├── config.py               # App settings loaded from .env
│   │   ├── db_async.py             # Async database engine and session
│   │   ├── db_sync.py              # Sync database engine for Alembic
│   │   ├── deps.py                 # FastAPI dependencies (auth, db, roles)
│   │   └── security.py             # Password hashing and JWT utilities
│   ├── models/
│   │   ├── users.py                # User ORM model
│   │   ├── course.py               # Course ORM model
│   │   └── enrollment.py           # Enrollment ORM model
│   ├── repositories/
│   │   ├── user.py                 # User database queries
│   │   ├── course.py               # Course database queries
│   │   └── enrollment.py           # Enrollment database queries
│   ├── schemas/
│   │   ├── auth.py                 # Token and login schemas
│   │   ├── user.py                 # User request/response schemas
│   │   ├── course.py               # Course request/response schemas
│   │   └── enrollment.py           # Enrollment request/response schemas
│   ├── services/
│   │   ├── auth_service.py         # Auth business logic
│   │   ├── user.py                 # User business logic
│   │   ├── course.py               # Course business logic
│   │   └── enrollment.py           # Enrollment business logic
│   └── main.py                     # FastAPI app entry point
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Fixtures and test database setup
│   ├── test_auth.py                # Auth endpoint tests
│   ├── test_courses.py             # Course endpoint tests
│   └── test_enrollments.py         # Enrollment endpoint tests
├── .env                            # Environment variables (not committed)
├── .dockerignore
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── requirements.txt
└── README.md


## Local Setup

### Prerequisites

- Python 3.11+
- PostgreSQL installed and running

### 1. Clone the repository

git clone <your-repo-url>
cd Course_Enrollment_Platform_API

### 2. Create and activate a virtual environment

python -m venv env

# Windows
env\Scripts\activate

# macOS/Linux
source env/bin/activate


### 3. Install dependencies

pip install -r requirements.txt

### 4. Configure environment variables

Create a `.env` file in the root directory:


DATABASE_URL_ASYNC=postgresql+asyncpg://postgres:yourpassword@localhost/Course_Enrollment_db
DATABASE_URL=postgresql://postgres:yourpassword@localhost/Course_Enrollment_db
ENVIRONMENT=DEBUG
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
PROJECT_NAME=Course_Enrollment_platform_api
API_PREFIX=/api/v1

> Generate a strong secret key with:
> 
> python -c "import secrets; print(secrets.token_hex(32))"
> 

### 5. Create the PostgreSQL database

createdb Course_Enrollment_db

Or in psql:

CREATE DATABASE "Course_Enrollment_db";


## Running Migrations

Apply all migrations to create the database tables:


alembic upgrade head

To generate a new migration after changing a model:


alembic revision --autogenerate -m "describe your change"
alembic upgrade head

To roll back one migration:


alembic downgrade -1


## Running the Server


uvicorn app.main:app --reload


The API will be available at:

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/api/v1/docs` | Swagger UI (interactive docs) |
| `http://127.0.0.1:8000/api/v1/redoc` | ReDoc documentation |
| `http://127.0.0.1:8000/api/v1/openapi.json` | OpenAPI schema |

## Docker Deployment

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### Build and start all services


docker-compose up --build

This single command will:
- Build the FastAPI app image
- Pull and start a PostgreSQL 15 container
- Automatically run all Alembic migrations
- Start the API server on port 8000

### Access the API

http://localhost:8000/api/v1/docs


### Other useful Docker commands

# Run in the background (detached mode)
docker-compose up --build -d

# View live logs
docker-compose logs -f api

# Stop all containers
docker-compose down

# Stop and remove volumes (wipes the database)
docker-compose down -v

# Rebuild after code changes
docker-compose up --build


### How it works

The `docker-compose.yml` defines two services:

- **db** — PostgreSQL 15 database with a persistent volume so data survives restarts
- **api** — FastAPI application that runs migrations automatically on startup

> The database URL inside Docker uses `@db` (the service name) instead of `@localhost` — this is how containers talk to each other inside Docker's internal network.


## Running Tests

Tests use an **in-memory SQLite database** — no PostgreSQL or Docker needed.

### Run all tests

pytest tests/ -v

### Run with coverage report


pytest tests/ -v --cov=app


### Run a specific test file


pytest tests/test_auth.py -v
pytest tests/test_courses.py -v
pytest tests/test_enrollments.py -v

## API Overview

### Auth

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/auth/register` | No | Register a new user |
| POST | `/api/v1/auth/login` | No | Login and receive JWT token |
| GET | `/api/v1/auth/me` | Yes | Get current user profile |

### Users

| Method | Endpoint | Auth | Role | Description |
|--------|----------|------|------|-------------|
| GET | `/api/v1/user/me` | Yes | Any | Get own profile |
| GET | `/api/v1/user/` | Yes | Admin | List all users |
| GET | `/api/v1/user/{id}` | Yes | Admin | Get user by ID |
| PATCH | `/api/v1/user/{id}` | Yes | Any* | Update user |
| DELETE | `/api/v1/user/{id}` | Yes | Admin | Delete user |

> *Users can only update their own profile. Admins can update any user.

### Courses

| Method | Endpoint | Auth | Role | Description |
|--------|----------|------|------|-------------|
| GET | `/api/v1/course/` | No | — | List all active courses |
| GET | `/api/v1/course/{id}` | No | — | Get course by ID |
| POST | `/api/v1/course/` | Yes | Admin | Create a course |
| PATCH | `/api/v1/course/{id}` | Yes | Admin | Update a course |
| DELETE | `/api/v1/course/{id}` | Yes | Admin | Delete a course |

### Enrollments

| Method | Endpoint | Auth | Role | Description |
|--------|----------|------|------|-------------|
| GET | `/api/v1/enrollment/me` | Yes | Student | View own enrollments |
| POST | `/api/v1/enrollment/` | Yes | Student | Enroll in a course |
| DELETE | `/api/v1/enrollment/{id}` | Yes | Student | Unenroll from a course |
| GET | `/api/v1/enrollment/` | Yes | Admin | View all enrollments |
| GET | `/api/v1/enrollment/course/{id}` | Yes | Admin | View enrollments for a course |
| DELETE | `/api/v1/enrollment/admin/{id}` | Yes | Admin | Remove a student from a course |


## Role-Based Access Control

| Action | Student | Admin |
|--------|:-------:|:-----:|
| View courses | ✅ | ✅ |
| Enroll in course | ✅ | ❌ |
| Deregister from course | ✅ | ❌ |
| Create course | ❌ | ✅ |
| Update course | ❌ | ✅ |
| Delete course | ❌ | ✅ |
| View all enrollments | ❌ | ✅ |
| Remove any enrollment | ❌ | ✅ |

### Enrollment Business Rules

- A student cannot enroll in the same course twice
- Enrollment is blocked if the course is at full capacity
- Enrollment is blocked if the course is inactive
- Students can only deregister from their own enrollments
- Admins can remove any enrollment


## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL_ASYNC` | Async PostgreSQL URL for the app | `postgresql+asyncpg://user:pass@localhost/dbname` |
| `DATABASE_URL` | Sync PostgreSQL URL for Alembic | `postgresql://user:pass@localhost/dbname` |
| `ENVIRONMENT` | Set to `DEBUG` to enable SQL logging | `DEBUG` |
| `SECRET_KEY` | JWT signing secret — keep this private | 64-character hex string |
| `ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | How long tokens stay valid | `30` |
| `PROJECT_NAME` | Displayed in API docs title | `Course_Enrollment_platform_api` |
| `API_PREFIX` | URL prefix applied to all routes | `/api/v1` |



deployment link:  courseenrollmentplatformapi-production.up.railway.app


Third semester exam from ALTSCHOOL AFRICA