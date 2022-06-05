FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install gcc -y
RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/