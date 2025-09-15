FROM python:3.8.18

# Install dependencies for node
RUN apt-get update && \
    apt-get install -y curl ca-certificates && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    node --version && npm --version

RUN apt-get -y install libcairo-dev
RUN mkdir -p /usr/src/app

COPY package.json /usr/src/app/
RUN npm --version
RUN npm install --prefix /usr/src/app/

COPY requirements.txt /usr/src/app
RUN pip install -r /usr/src/app/requirements.txt

COPY . /usr/src/app
WORKDIR /usr/src/app
RUN npm run-script build-jobs

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
