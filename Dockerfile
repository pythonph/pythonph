FROM python:2.7.17

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get -y install nodejs
RUN apt-get -y install libcairo-dev

RUN mkdir -p /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install -r /usr/src/app/requirements.txt

WORKDIR /usr/src/app
COPY . /usr/src/app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
