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
| Editor/Rich Text | TinyMCE (django-tinymce)                                                                        |
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

## Media Storage (Cloudflare R2)

Uploaded media (event cover images, volunteer/team photos) is stored in
[Cloudflare R2](https://django-storages.readthedocs.io/en/latest/backends/s3_compatible/cloudflare-r2.html)
via `django-storages` + `boto3`. Static files are unaffected and stay on
WhiteNoise.

When the R2 credentials below are set, Django's default storage becomes the
S3-compatible `S3Boto3Storage` backend pointed at your bucket. When they are
missing (e.g. local development), it falls back to the local filesystem
(`MEDIA_ROOT` / `mediafiles/`).

Add these to your `.env` (or Render env vars):

```bash
R2_ACCOUNT_ID=your-account-id
R2_ACCESS_KEY_ID=your-access-key-id
R2_SECRET_ACCESS_KEY=your-secret-access-key
R2_BUCKET_NAME=pythonph-media
R2_PUBLIC_URL=media.python.ph   # optional: custom domain
```

Setup steps:

1. Create an R2 bucket in the Cloudflare dashboard.
2. Create an API token with **Object Read & Write** permission scoped to that bucket.
3. Make the bucket publicly accessible (public bucket or a custom domain) so
   `AWS_QUERYSTRING_AUTH=False` serves files without signed URLs.
4. Set `R2_PUBLIC_URL` to your custom domain to serve uploaded files from it;
   leave it blank to use the bucket's r2.dev URL.

## Deployment

Deployed on [Render](https://render.com/). See `render.yaml` for service
configuration. The build process:

1. Install dependencies with `uv sync`
