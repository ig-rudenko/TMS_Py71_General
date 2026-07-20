FROM python:3.14.6-alpine

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY django_project /app
