FROM python:3.8.1

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get -y install nodejs
RUN apt-get -y install libcairo-dev

RUN mkdir -p /usr/src/app

COPY package.json /usr/src/app/
RUN npm install --prefix /usr/src/app/

COPY requirements.txt /usr/src/app
RUN pip install -r /usr/src/app/requirements.txt

COPY . /usr/src/app
WORKDIR /usr/src/app
RUN npm run-script build-jobs

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
