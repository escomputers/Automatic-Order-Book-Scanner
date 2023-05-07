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
# RUN wget https://raw.githubusercontent.com/escomputers/Automatic-Order-Book-Scanner/58eeeeb132c5f1f5430831696644ba3b88ef7da8/babsproj/requirements.txt
RUN python -m pip install -r /app/requirements.txt
