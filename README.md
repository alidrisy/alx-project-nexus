# JobBoard Backend (ProDev BE)

Backend API for a Job Board Platform using Django, DRF, JWT, and PostgreSQL with role-based access control and Swagger docs.

## Features
- Custom user with roles: ADMIN, RECRUITER, USER
- JWT auth (`/api/auth/token/`, `/api/auth/token/refresh/`)
- Jobs CRUD, Categories CRUD, Applications
- RBAC via DRF permissions
- Filtering, search, ordering on jobs
- Swagger UI at `/api/docs/`

## Quickstart (Local)
1. Create virtualenv and install deps
```
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```
2. Configure Postgres via env (or edit `jobboard/settings.py`)
```
export POSTGRES_DB=jobboard
export POSTGRES_USER=jobboard
export POSTGRES_PASSWORD=jobboard
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export DJANGO_SECRET_KEY=dev-secret-key
export DJANGO_DEBUG=1
```
3. Run migrations and create superuser
```
python manage.py migrate
python manage.py createsuperuser
```
4. Run the server
```
python manage.py runserver 0.0.0.0:8000
```

## API
- Auth: `POST /api/auth/token/` (username, password) → access/refresh tokens
- Docs: `GET /api/docs/`
- Jobs: `GET /api/jobs/`, `POST /api/jobs/`, `GET /api/jobs/{id}/`, `PATCH /api/jobs/{id}/`, `DELETE /api/jobs/{id}/`
- Categories: `GET /api/jobs/categories/`, `POST /api/jobs/categories/` (ADMIN)
- Apply: `POST /api/jobs/{id}/apply/` (USER)
- Applications: `GET /api/jobs/applications/` (own/admin)

## Notes
- Set `AUTH_USER_MODEL = 'accounts.User'`
- Update DB indexes later for search performance (GIN/pg_trgm).

## Docker (recommended)
1. Ensure Docker is running.
2. Create a `.env` file (copy from `.env.example`):
```
DJANGO_SECRET_KEY=dev-secret-key
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=*
POSTGRES_DB=jobboard
POSTGRES_USER=jobboard
POSTGRES_PASSWORD=jobboard
POSTGRES_HOST=db
POSTGRES_PORT=5432
USE_SQLITE=0
```
3. Build and start:
```
docker compose up --build
```
4. Access:
- API: http://localhost:8000/
- Swagger: http://localhost:8000/api/docs/
- Admin: http://localhost:8000/admin/

To run with SQLite inside the container, set `USE_SQLITE=1` and remove the `db` dependency, but Postgres is recommended.

```

