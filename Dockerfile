FROM python:3.7-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-libs postgresql-dev libffi-dev \
       openldap-dev unixodbc-dev gcc musl-dev python3-dev \
       jpeg-dev zlib-dev libjpeg

COPY ./requirements.txt .

RUN pip install -r /requirements.txt

RUN mkdir /app
COPY . /app/
WORKDIR /app
RUN cd /app

