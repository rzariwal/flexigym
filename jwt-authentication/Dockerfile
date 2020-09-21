# pull official base image
FROM python:3.6.10-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc netcat
RUN pip install --upgrade pip
RUN apt-get install -y dos2unix
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/
#RUN dos2unix /usr/src/app/*
# run entrypoint.sh
ENTRYPOINT ["sh","/usr/src/app/entrypoint.sh"]
#CMD ["python", "manage.py", "test"]
