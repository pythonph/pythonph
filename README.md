# PythonPH

## Development Setup

1. Create `.env` (see `config/environment.py` for all options)

```bash
SECRET_KEY=secret
APP_ENV=development
DEBUG=true
SLACK_ORG=pythonph
SLACK_API_TOKEN=xxxx-xxxxxxxxxx-xxxxxxxxxx-xxxxxxxxxxx-xxxxxxxxxx
SLACK_BOARD_CHANNEL=pythonph
SLACK_JOBS_CHANNEL=jobs
```

2. Install dependencies (uses [uv](https://docs.astral.sh/uv/))

```bash
make install-dev
```

3. Setup the database (SQLite in development)

```bash
make setup-db
uv run python manage.py createsuperuser
```

4. Set up Tailwind CSS (one-time download of the standalone CLI — no Node.js needed)

```bash
make run-tailwind-setup
```

5. Run the dev server with Tailwind watching for changes

```bash
make run-server-tailwind
```

## Frontend

This project uses Tailwind CSS v4 with DaisyUI, built via
[`django-tailwind-cli`](https://django-tailwind-cli.andolino.io/) (no Node.js
required). The source stylesheet is `src/styles/main.css` and the compiled
output is `static/css/app.css` (gitignored, built during deploy).

```bash
make run-tailwind-watch   # watch mode during development
make run-tailwind-build   # production build (minified)
```

## Development Setup via docker-compose

1. `./bin/build-dev`
2. `./bin/deploy-dev`

Note: For this setup, you have to run `./bin/build-dev && ./bin/deploy-dev` for changes to reflect.

## Todo

1. Improve dockerized development setup
