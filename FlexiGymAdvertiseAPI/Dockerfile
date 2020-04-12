FROM python:3-alpine

MAINTAINER Ehkalu

COPY ./myapp/requirements.txt /myapp/requirements.txt

WORKDIR /myapp

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

COPY ./myapp/package.json /myapp/package.json

RUN npm install

COPY ./myapp /myapp

CMD ["python", "app.py"]