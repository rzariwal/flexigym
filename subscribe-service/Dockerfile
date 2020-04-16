FROM python:3-alpine

MAINTAINER Sandeep Bogaram

COPY ./service/requirements.txt /service/requirements.txt

WORKDIR /service


RUN apk add --update \
    py3-mysqlclient \
    && pip install --upgrade pip  \
    && pip install -r requirements.txt \
    && rm -rf /var/cache/apk/*

COPY ./service/package.json /service/package.json

COPY ./service /service

CMD ["python", "app.py"]