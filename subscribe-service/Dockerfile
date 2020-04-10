FROM python:3-alpine

MAINTAINER Sandeep Bogaram

COPY ./requirements.txt /requirements.txt

WORKDIR /


RUN apk add --update \
    py3-mysqlclient \
    && pip install --upgrade pip  \
    && pip install -r requirements.txt \
    && rm -rf /var/cache/apk/*

#COPY ./package.json /package.json

COPY ./ /

CMD ["python", "app.py"]