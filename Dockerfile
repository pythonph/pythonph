FROM nikolaik/python-nodejs:python3.8-nodejs12

WORKDIR /usr/src/app

COPY . /usr/src/app/
RUN pip install -r requirements/docker.txt \
    && npm install \
    && npm run build-jobs \
    && python manage.py compress --force \
    && python manage.py collectstatic --noinput

COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 8000
CMD ["runprod"]
