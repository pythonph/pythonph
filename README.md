# PythonPH

## Development Setup via virtualenv

1. Make a copy of `.env.virtualenv` as `.env`.

```bash
$ cp .env.virtualenv .env
```

2. Create and activate your virtualenv.

```bash
$ virtualenv venv
$ source venv/bin/activate
```

3. Install python packages.

```bash
$ pip install -r requirements/virtualenv.txt
```

4. Run Django migrations.

```bash
$ python manage.py migrate
```

5. Run Django server.

```bash
$ python manage.py runserver
```

6. Install npm packages and run build watcher (Optional, only run if you need to work on JS).

```bash
$ npm install
$ npm run dev
```

## Development Setup via docker-compose

1. Make a copy of `.env.docker` as `.env`.

```bash
$ cp .env.docker .env
```

2. Build images and run containers.

```bash
$ docker-compose build
$ docker-compose up -d
```

3. Run migrations

```bash
$ docker-compose run --rm web migrate
```

4. Running Django's manage.py to run other commands

```bash
$ docker-compose run --rm web python manage.py <command>
```
