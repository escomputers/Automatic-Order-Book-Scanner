# syntax=docker/dockerfile:1
FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1

# install app dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc python3-pip

# install app
RUN mkdir -p /app
WORKDIR /app
COPY . /app
COPY requirements.txt /app/requirements.txt
RUN python -m pip install -r /app/requirements.txt
