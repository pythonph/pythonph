PYTHON=uv run python
MANAGE=manage.py

run:
	$(PYTHON) $(MANAGE) runserver

run-gunicorn:
	uv run gunicorn config.wsgi:application -b 0.0.0.0:8000

setup-db:
	$(PYTHON) $(MANAGE) makemigrations
	$(PYTHON) $(MANAGE) migrate

check:
	$(PYTHON) $(MANAGE) check

shell:
	$(PYTHON) $(MANAGE) shell

test:
	$(PYTHON) $(MANAGE) test

collectstatic:
	$(PYTHON) $(MANAGE) collectstatic --noinput

createcachetable:
	$(PYTHON) $(MANAGE) createcachetable

run-pre-commit:
	uv run pre-commit run --all-files

run-ruff:
	uv run ruff check . && \
	uv run ruff format .

run-ruff-fix:
	uv run ruff check --fix . && \
	uv run ruff format .

install:
	uv sync

install-dev:
	uv sync --dev

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
