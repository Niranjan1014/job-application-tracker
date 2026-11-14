# Job Application Tracking Platform

A FastAPI REST API for managing job applications with individual user accounts, JWT authentication, PostgreSQL persistence, and status tracking.

## Features

- User registration and JWT-based login
- Password hashing with bcrypt
- Authenticated application CRUD
- Per-user data isolation (users can only access their own applications)
- Filter by application status and company
- Pagination
- Request validation with Pydantic
- Automated tests and GitHub Actions CI

## Tech stack

Python 3.11+, FastAPI, SQLAlchemy 2, PostgreSQL, Pydantic, JWT (python-jose), Passlib/bcrypt, pytest.

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a PostgreSQL database and copy `.env.example` to `.env`. Set a strong, unique `SECRET_KEY` and your database URL.
4. Create database tables for this development version:

   ```bash
   python -c "from app.database import Base, engine; import app.models.user, app.models.application; Base.metadata.create_all(bind=engine)"
   ```

5. Start the API:

   ```bash
   uvicorn app.main:app --reload
   ```

6. Open interactive API docs at http://127.0.0.1:8000/docs.

## API overview

| Method | Endpoint | Description |
|---|---|---|
| POST | /auth/register | Create an account |
| POST | /auth/login | Get a JWT (OAuth2 form: username=email, password=...) |
| POST | /applications/ | Create an application (Bearer token required) |
| GET | /applications/ | List your applications; optional status, company, page, page_size |
| PATCH | /applications/{id} | Update your application |
| DELETE | /applications/{id} | Delete your application |
| GET | /health | Health check |

## Run tests

The tests use an isolated in-memory SQLite database:

```bash
pytest -q
```

## Security notes

- Use a long random secret key in `.env`; never commit real credentials.
- Passwords are stored as bcrypt hashes, never as plain text.
- Application queries are scoped to the authenticated user's ID.
- This is a learning/demo backend. Before production deployment, add Alembic migrations, rate limiting, stricter email validation, structured logging, HTTPS, and deployment secrets management.
