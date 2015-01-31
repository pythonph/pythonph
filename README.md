# PythonPH Jobs

## Development Setup

```bash
export DEBUG=True
export SECRET_KEY=secret
export POSTGRES_USER=jobs
export POSTGRES_PASSWORD=password
```

### PostgreSQL

```bash
createuser -P jobs
# You will be prompted to enter a password
# Enter what you set in POSTGRES_PASSWORD
createdb -O jobs jobs
```

### Virtualenv

```bash
mkvirtualenv jobs
pip install -r requirements.txt
```

### Frontend

```bash
npm install
bower install
npm run build
```

### Django

```
python manage.py migrate
python manage.py runserver
```
