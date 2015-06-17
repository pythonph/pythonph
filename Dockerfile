FROM python:2.7.7

RUN curl -sL https://deb.nodesource.com/setup | bash -
RUN apt-get -y install nodejs
RUN apt-get -y install libcairo-dev

RUN pip install virtualenv

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

ENTRYPOINT ["./docker-entrypoint"]

