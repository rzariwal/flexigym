FROM python:3-alpine

MAINTAINER Ehkalu

COPY ./api/requirements.txt /api/requirements.txt

WORKDIR /api

RUN apk add --update \
    py3-mysqlclient \
    gcc \
    libc-dev \
    mariadb-dev \
    nodejs \
    npm \
    && pip install --upgrade pip  \
    && pip install -r requirements.txt \
    && rm -rf /var/cache/apk/*

COPY ./api/package.json /api/package.json

RUN npm install

COPY ./api /api

CMD ["python", "app.py"]