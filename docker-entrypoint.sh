#!/usr/bin/env sh
set -e

if [ "$1" = "migrate" ]; then
  python manage.py migrate
  exit 0
fi

if [ "$1" = "makemigrations" ]; then
  python manage.py makemigrations
  exit 0
fi

if [ "$1" = "createsuperuser" ]; then
  python manage.py createsuperuser
  exit 0
fi

if [ "$1" = "rundev" ]; then
  npm run dev & python manage.py runserver 0.0.0.0:8000
  exit 0
fi

if [ "$1" = "runprod" ]; then
  gunicorn -b 0.0.0.0:8000 --access-logfile - --error-logfile - pythonph.wsgi
  exit 0
fi

exec "$@"
