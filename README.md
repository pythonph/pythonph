# PythonPH

## Development Setup

```bash
export DEBUG=True
export SECRET_KEY=secret
export POSTGRES_USER=pythonph
export POSTGRES_PASSWORD=password
```

### PostgreSQL

```bash
createuser -P pythonph
# You will be prompted to enter a password
# Enter what you set in POSTGRES_PASSWORD
createdb -O pythonph pythonph
```

### Virtualenv

```bash
mkvirtualenv pythonph
pip install -r requirements.txt
```

### Django

```
python manage.py migrate
python manage.py runserver
```
