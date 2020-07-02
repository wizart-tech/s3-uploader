FROM python:3-alpine

COPY ./app/requirements.txt /app/

RUN pip3 install -r /app/requirements.txt

COPY ./app /app

WORKDIR /app
