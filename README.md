# PythonPH

Python Philippines community website — built with Django 5.2, Tailwind CSS v4,
and DaisyUI.

## Tech Stack

| Layer            | Technology                                                                                      |
| ---------------- | ----------------------------------------------------------------------------------------------- |
| Backend          | Django 5.2, Django REST Framework, Pydantic Settings                                            |
| Frontend         | Tailwind CSS v4 + [DaisyUI](https://daisyui.com/) via `django-tailwind-cli` (no Node.js needed) |
| Database         | SQLite (dev) / PostgreSQL (prod)                                                                |
| Static Files     | WhiteNoise (with Brotli compression)                                                            |
| ASGI/WSGI        | Gunicorn (WSGI) / Django ASGI                                                                   |
| Error Tracking   | Sentry SDK                                                                                      |
| Editor/Rich Text | CKEditor 4, django-markdownx                                                                    |
| Task Runner      | GNU Make + uv                                                                                   |
| Linting          | Ruff, pre-commit                                                                                |
| Deploy           | Render (via `deploy/build.sh` + `deploy/start.sh`)                                              |

## Apps

| App                | Description                                                            |
| ------------------ | ---------------------------------------------------------------------- |
| `app.landing`      | Public landing page with team, mission, and CTA sections               |
| `app.registration` | User registration and authentication (Django auth views)               |
| `app.jobs`         | Job board — companies post jobs, public listing with tags & pagination |
| `app.organisation` | Committee & volunteer management                                       |

## Development Setup

1. **Create `.env`** (see `config/environment.py` for all options)

```bash
SECRET_KEY=secret
APP_ENV=development
DEBUG=true
```

2. **Install dependencies** (uses [uv](https://docs.astral.sh/uv/), Python >= 3.13)

```bash
make install-dev
```

3. **Set up the database** (SQLite in development)

```bash
make setup-db
uv run python manage.py createsuperuser
```

4. **Set up Tailwind CSS** (one-time download of the standalone CLI — no Node.js needed)

```bash
make run-tailwind-setup
```

5. **Run the dev server** with Tailwind watching for changes

```bash
make run-server-tailwind
```

The site will be available at <http://localhost:8000>.

## Development Commands

```bash
make run            # Run Django dev server
make shell          # Django shell
make test           # Run tests
make check          # Django system checks
make collectstatic  # Collect static files
make createcachetable # Create cache table
make run-ruff       # Lint & format check (Ruff)
make run-ruff-fix   # Auto-fix lint/format issues
make run-pre-commit # Run pre-commit hooks on all files
make clean          # Remove __pycache__ and .pyc files
```

## Frontend

The source stylesheet is `src/styles/main.css` (Tailwind v4 + DaisyUI). The
compiled output (`static/css/app.css`) is gitignored and built during deploy.

```bash
make run-tailwind-watch   # Watch mode during development
make run-tailwind-build   # Production build (minified)
```

> **Note:** The codebase has a mix of styling approaches — the landing page uses a
> committed prebuilt CSS blob (Bootstrap 5 + Tailwind v2), while the jobs and auth
> pages use SCSS via django-compressor. The `django-tailwind-cli` setup is the
> current/modern path forward.

## API

The jobs app exposes a REST API under `/jobs/api/v1/` (Django REST Framework).

- `GET /jobs/api/v1/jobs` — list approved, active jobs
- `GET /jobs/api/v1/companies` — list companies

## Health Check

A `GET /health` endpoint returns `200 OK` — useful for load balancer or
monitoring probes.

## Docker

### Development

```bash
./bin/build-dev    # Build the image + nginx
./bin/deploy-dev   # Start containers (web, nginx, db, source)
```

### Production

```bash
./bin/build        # Build the image + nginx
./bin/deploy       # Deploy (web, nginx)
```

Note: For the dockerized development setup, run `./bin/build-dev && ./bin/deploy-dev` for changes to reflect.

## Deployment

Deployed on [Render](https://render.com/). See `render.yaml` for service
configuration. The build process:

1. Install dependencies with `uv sync`
