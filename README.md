# Job Application Tracking Platform

A full-featured REST API backend for tracking job applications across multiple stages, with JWT authentication and role-based access control.

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL + SQLAlchemy ORM
- **Auth:** JWT (OAuth2 Password Bearer)
- **Migrations:** Alembic
- **CI/CD:** GitHub Actions
- **Containerization:** Docker

## Features

- User registration and JWT login
- Role-based access (admin / user)
- Full CRUD for job applications
- Application status tracking (Applied → Screening → Interview → Offer → Rejected)
- Filtering by status, company, date range
- Pagination on all list endpoints
- Automated test suite with GitHub Actions CI

## Project Structure

```
job-application-tracker/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Settings via pydantic-settings
│   ├── database.py          # DB session and engine
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── routers/             # API route handlers
│   └── services/            # Business logic layer
├── tests/
│   └── test_applications.py
├── alembic/                 # DB migrations
├── docker/
│   └── docker-compose.yml
├── .github/workflows/
│   └── ci.yml
├── requirements.txt
└── .env.example
```

## Setup

```bash
git clone https://github.com/Niranjan1014/job-application-tracker.git
cd job-application-tracker
cp .env.example .env
docker compose -f docker/docker-compose.yml up -d
uvicorn app.main:app --reload
# Docs at http://localhost:8000/docs
```
