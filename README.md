# PythonPH Jobs

## Setup

### PostgreSQL

```bash
export POSTGRES_USER=jobs
export POSTGRES_PASSWORD=password
createuser -P jobs
# You will be prompted to enter a password
# Enter what you set in POSTGRES_PASSWORD
createdb -O jobs jobs
```

### Django

```bash
mkvirtualenv jobs
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
