FROM python:3.13-slim

WORKDIR /usr/src/app

# Install UV
RUN pip install --upgrade pip && pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application
COPY . .

# Collect static files
RUN uv run manage.py collectstatic --noinput

CMD ["gunicorn", "config.wsgi:application", "-b", "0.0.0.0:8000"]
