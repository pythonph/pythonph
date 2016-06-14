# PythonPH

## Development Setup

1. Setup db

  ```bash
  createuser -P pythonph
  # You will be prompted to enter a password
  # Enter what you set in POSTGRES_PASSWORD
  createdb -O pythonph pythonph
  ```

2. Setup virtualenv

  ```bash
  mkvirtualenv venv
  venv/bin/pip install -r requirements.txt
  ```

3. Setup npm

  ```bash
  npm install
  ```

4. Create `dev.env`

  ```bash
  SECRET_KEY=secret
  ENV=DEV
  POSTGRES_USER=pythonph
  POSTGRES_PASSWORD=password
  SLACK_ORG=pythonph
  SLACK_API_KEY=xxxx-xxxxxxxxxx-xxxxxxxxxx-xxxxxxxxxxx-xxxxxxxxxx
  ```

5. Setup Django

  ```bash
  bin/localmanage migrate
  bin/localmanage createsuperuser
  ```

6. Run server

  ```bash
  npm start
  ```

